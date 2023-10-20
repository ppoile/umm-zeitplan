# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import logging


class Gruppe:
    def __init__(self, name):
        self._name = name
        logging.debug("    gruppe: %s", name)

    @property
    def name(self):
        return self._name
