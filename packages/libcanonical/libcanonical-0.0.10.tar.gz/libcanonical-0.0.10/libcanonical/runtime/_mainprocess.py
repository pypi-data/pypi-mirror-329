# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import inspect
import logging.config
import signal
import time
import os
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import TypeVar

import pydantic

from libcanonical.environ import EnvironmentVariables
from libcanonical.utils import logger
from ._logging import LOGGING_CONFIG


R = TypeVar('R')


class MainProcess:
    """The main process of an application."""
    environment: type[EnvironmentVariables] = EnvironmentVariables
    handle_signals: bool = True
    interval: float = 0.01
    logger = logger
    log_tracebacks: bool = True
    min_runtime: int = 0
    must_drop: bool = True
    must_exit: bool = False
    must_reload: bool = False
    uid: int
    _step: int = 0

    @property
    def step(self) -> int:
        return self._step

    @classmethod
    def run(cls, name: str):
        self = cls(
            name=name
        )
        self.main()

    def __init__(self, name: str):
        self.name = name
        self.environ = self.environment.parse(self.name)

    def configure(self, reloading: bool = False) -> None | Coroutine[None, None, None]:
        """A hook to configure and setup the process, prior to entering the
        main event loop. This method is also invoked when the application is
        requested to reload using ``SIGHUP``.

        Args:
            reloading (bool): indicates if this method was invoked during
                a reload. If `reloading` is ``False``, then the main event
                loop is not running.

        Returns:
            None
        """
        pass

    def get_logging_config(self) -> dict[str, Any]:
        return LOGGING_CONFIG

    def initialize(self) -> None:
        """Initializes the application on the current system."""
        return

    def is_initialized(self):
        """Return a boolean indicating if the application is initialized."""
        return all([
            os.path.exists(self.environ.vardir)
        ])

    def is_stopped(self):
        return self.must_exit

    def log_step(self, duration: float):
        self.logger.debug(
            "Completed main event in %.02fs (step: %s)",
            duration,
            self.step
        )

    def main(self) -> None:
        if self.handle_signals:
            self._bind_signal_handlers()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.__main__())

    def main_event(self) -> None | Coroutine[None, None, None]:
        """The main event of the process. Subclasses must override
        this method.
        """
        raise NotImplementedError

    def on_completed(self):
        """A hook that is invoked when the process exits succesfully."""
        return

    def on_sigint(self) -> None:
        """Invoked when the process receives a ``SIGINT`` signal."""
        self.logger.info("Caught SIGINT (pid: %s)", os.getpid())
        if self.must_exit:
            # If we already received a SIGINT, assume that the
            # process is not existing and the user wants to
            # kill it off.
            os.kill(os.getpid(), signal.SIGKILL)
        self.must_exit = True

    def on_sighup(self) -> None:
        """Invoked when the process receives a ``SIGHUP`` signal."""
        self.must_reload = True

    def on_sigterm(self) -> None:
        """Invoked when the process receives a ``SIGTERM`` signal."""
        # TODO: Implement this as must_kill
        self.must_exit = True

    def on_sigusr1(self) -> None:
        """Hook to handle ``SIGUSR1``. Subclasses may override this method
        without calling :func:`super()`.
        """
        pass

    def on_sigusr2(self) -> None:
        """Hook to handle ``SIGUSR2``. Subclasses may override this method
        without calling :func:`super()`.
        """
        pass

    def setup_logging(self):
        """Configures the loggers for the application."""
        logging.config.dictConfig(self.get_logging_config())

    def stop(self):
        self.must_exit = True

    def teardown(self) -> None | Coroutine[None, None, None]:
        """Called during application teardown. Subclasses may override
        this method without calling :func:`super()`.
        """
        pass

    async def __main__(self) -> None:
        if not (await self._run(self._configure)):
            self.logger.critical("Failed configuration, exiting main event loop.")
            await asyncio.sleep(5)
            return
        self.logger.debug("Starting main event loop")
        if self.uid == 0:
            self.logger.warning("This process is running as a privileged user.")
        while True:
            await asyncio.sleep(self.interval)
            t0 = time.time()
            if self.must_exit:
                self.logger.info(
                    "Shutting down %s (pid: %s)",
                    self.name,
                    self.pid
                )
                await self._teardown()
                break
            if self.must_reload:
                self.logger.warning("Reloading %s (pid: %s)", self.name, self.pid)
                await self._run(self._configure, reloading=True)
            self._step += 1
            try:
                await self._run(self.main_event)
            except Exception as e:
                self._log_exception(e)
                await asyncio.sleep(1)
            finally:
                duration = time.time() - t0
                self.log_step(duration)
                t = self.min_runtime - duration
                if t > 0:
                    self.logger.debug("Sleeping for %s seconds.", t)
                    await asyncio.sleep(t)

    def _bind_signal_handlers(self):
        signal.signal(signal.SIGHUP, lambda s, f: self.on_sighup())
        signal.signal(signal.SIGINT, lambda s, f: self.on_sigint())
        signal.signal(signal.SIGUSR1, lambda s, f: self.on_sigusr1())
        signal.signal(signal.SIGUSR2, lambda s, f: self.on_sigusr2())

    def _configure(self, reloading: bool = False):
        self.setup_logging()
        self.uid = os.getuid()
        self.pid = os.getpid()
        if not reloading and not self.is_initialized():
            self._initialize()
        try:
            self.configure(reloading=reloading)
            success = True
        except Exception as e:
            self._log_exception(e)
            success = False
        finally:
            self.must_reload = False
        return success

    def _initialize(self):
        if not os.access(self.environ.vardir.parent, os.W_OK):
            self.logger.critical(
                "Unable to create state directory %s",
                self.environ.vardir
            )
            self.stop()
        if self.is_stopped():
            return
        if not os.path.exists(self.environ.vardir):
            os.makedirs(self.environ.vardir, exist_ok=True)
        self.initialize()

    def _log_exception(self, e: BaseException, *args: Any, **kwargs: Any):
        self.logger.error(
            "Caught %s",
            type(e).__name__
        )
        if self.log_tracebacks:
            self.logger.exception("The traceback was:")

    async def _run(
        self,
        func: Callable[..., R | Awaitable[R]],
        *args: Any,
        **kwargs: Any
    ):
        result = func(*args, **kwargs)
        if inspect.iscoroutinefunction(func):
            assert inspect.isawaitable(result)
            result = await result
        return result

    async def _teardown(self):
        try:
            await self._run(self.teardown)
            await self._run(self.on_completed)
        except Exception as e:
            self._log_exception(e)