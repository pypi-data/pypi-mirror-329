from typing import Optional, List

from . import MagicCommand
from .StringWrapper import StringWrapper


class MagicCommandCallback:
    def __init__(self, mc: MagicCommand, silent: bool, code: StringWrapper, *args, **kwargs):
        self._mc: MagicCommand = mc
        self._silent: bool = silent
        self._code: StringWrapper = code
        self._args = args
        self._kwargs = kwargs

    @property
    def magic(self) -> MagicCommand:
        return self._mc

    def __call__(self, columns: Optional[List[str]] = None, rows: Optional[List[List]] = None):
        if self._mc.requires_code:
            result = self._mc(self._silent, self._code.value, *self._args, **self._kwargs)
            if 'generated_code' in result:
                self._code.value = result['generated_code']

            return result

        if self._mc.requires_query_result:
            return self._mc(self._silent, columns, rows, *self._args, **self._kwargs)

        else:
            return self._mc(self._silent, *self._args, **self._kwargs)
