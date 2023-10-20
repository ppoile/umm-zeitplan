# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import logging


class Disziplin:
    def __init__(self, data):
        self._data = data

    @property
    def together(self):
        return self._data.get("together", False)

    @property
    def force_length(self):
        return self._data.get("force_length", False)
