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
import signal
import os
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import TypeVar

from libcanonical.utils import logger


R = TypeVar('R')


class MainProcess:
    """The main process of an application."""
    handle_signals: bool = True
    interval: float = 0.01
    logger = logger
    log_tracebacks: bool = True
    must_exit: bool = False
    must_reload: bool = False
    _step: int = 0

    @property
    def step(self) -> int:
        return self._step

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
        return self.on_sigint()

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

    def teardown(self) -> None | Coroutine[None, None, None]:
        """Called during application teardown. Subclasses may override
        this method without calling :func:`super()`.
        """
        pass

    async def __main__(self) -> None:
        await self._run(self._configure)
        while True:
            await asyncio.sleep(self.interval)
            if self.must_exit:
                await self._teardown()
                break
            if self.must_reload:
                await self._run(self._configure, reloading=True)
            self._step += 1
            try:
                await self._run(self.main_event)
            except Exception as e:
                self._log_exception(e)
                await asyncio.sleep(1)


    def _bind_signal_handlers(self):
        signal.signal(signal.SIGHUP, lambda s, f: self.on_sighup())
        signal.signal(signal.SIGINT, lambda s, f: self.on_sigint())
        signal.signal(signal.SIGUSR1, lambda s, f: self.on_sigusr1())
        signal.signal(signal.SIGUSR2, lambda s, f: self.on_sigusr2())

    def _configure(self, reloading: bool = False):
        try:
            return self.configure(reloading=reloading)
        except Exception as e:
            self._log_exception(e)
        finally:
            self.must_reload = False

    def _log_exception(self, e: BaseException, *args: Any, **kwargs: Any):
        self.logger.critical(
            "Caught %s during configure()",
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


class T(MainProcess):

    async def main_event(self) -> None:
        return None
    

T().main()