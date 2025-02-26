from typing import Dict, Union, TypeVar, cast
from os import environ, chdir, makedirs
from json import loads

ArgTypeGeneric = TypeVar("ArgTypeGeneric", int, float, str, bool, None)


class ScriptService:
    def __init__(self, mock: Union[Dict[str, Union[int, float, bool, str]], None]):
        self._run_id = environ.get('id', None)
        self._is_run_by_service = self._run_id is not None
        if self._is_run_by_service:
            makedirs(self._run_id, exist_ok=True)
            chdir(self._run_id)
        else:
            self._run_id = None

        self._mock = mock if mock is not None else {}
        params = environ.get('params', None)
        self._run_params = loads(params) if params is not None else {}

    def get_property(self, name: str) -> ArgTypeGeneric:
        if self._is_run_by_service:
            if name not in self._run_params:
                raise KeyError(f'Run property not exists: {name}')
            return cast(ArgTypeGeneric, self._run_params[name])
        else:
            return self._mock[name] if name in self._mock else None

    @property
    def run_id(self):
        return self._run_id

    @property
    def is_run_by_service(self):
        return self._is_run_by_service
