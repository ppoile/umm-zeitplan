# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import logging


class Gruppe:
    def __init__(self, name, scenario):
        self._name = name
        self._scenario = scenario
        self._disziplinen = []
        logging.debug("    gruppe: %s", name)
        self._create_resource()

    def _create_resource(self):
        self._resource = self._scenario.Resource(self.name)

    @property
    def name(self):
        return self._name

    @property
    def disziplinen(self):
        return self._disziplinen

    @property
    def resource(self):
        return self._resource
