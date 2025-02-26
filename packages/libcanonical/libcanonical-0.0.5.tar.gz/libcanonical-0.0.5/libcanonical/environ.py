# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import pathlib

import pydantic


class EnvironmentVariables(pydantic.BaseModel):
    name: str = pydantic.Field(
        default=...
    )

    loglevel: str = pydantic.Field(
        alias='LOGLEVEL',
        default='INFO'
    )

    vardir: pathlib.Path = pydantic.Field(
        alias='APP_VARDIR',
        default=...
    )

    @pydantic.model_validator(mode='before')
    def validate_params(cls, params: dict[str, str]):
        name = params.get('name')
        if not isinstance(name, str):
            raise pydantic.ValidationError()
        if not params.get('APP_VARDIR'):
            params['APP_VARDIR'] = f'/var/lib/{name}'
        return params

    @classmethod
    def parse(cls, app_name: str):
        return cls.model_validate({**os.environ, 'name': app_name})


defaults = EnvironmentVariables.parse('.canonical')