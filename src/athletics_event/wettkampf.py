# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import logging


class Wettkampf:
    def __init__(self, wettkampf_name, wettkampf_data, teilnehmer_data):
        self._wettkampf_name = wettkampf_name
        self._wettkampf_data = wettkampf_data[self.name]
        self._teilnehmer_data = teilnehmer_data[self.name]
        logging.debug("  wettkampf: %s", self.name)

    @property
    def name(self):
        return self._wettkampf_name

    @property
    def is_wettkampf_with_strict_sequence(self):
        return self._wettkampf_data.get("is_wettkampf_with_strict_sequence", False)

    @property
    def is_last_wettkampf_of_the_day(self):
        return self._wettkampf_data.get("is_last_wettkampf_of_the_day", False)

    @property
    def gruppen(self):
        return list(self._teilnehmer_data.keys())

    @property
    def disziplinen(self):
        return self._wettkampf_data["disziplinen"]
