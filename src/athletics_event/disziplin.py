# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

from collections import defaultdict
import logging
import math

from . import common


class Disziplin:
    def __init__(self, definition, wettkampf, gruppe, wettkampf_data, teilnehmer_data, scenario, offset):
        self._definition = definition
        self._wettkampf = wettkampf
        self._gruppe = gruppe
        self._wettkampf_data = wettkampf_data
        self._teilnehmer_data = teilnehmer_data
        self._scenario = scenario
        self._new_offset = None
        self._task = None
        self._interval_gruppen_names = []
        self.evaluate_full_name_and_num_athletes()
        self.evaluate_length(offset)
        self.create_task_if_necessary()

    def is_first_gruppe_of_interval(self):
        return self._gruppe.name == self._interval_gruppen_names[0]

    def evaluate_full_name_and_num_athletes(self):
        gruppen_names = self._wettkampf.gruppen
        if self.together:
            if self.keep_groups_separate:
                self._interval_gruppen_names = self._get_interval_gruppen(self._wettkampf.name, self._gruppe.name, gruppen_names, self._teilnehmer_data, self._definition)
                if len(self._interval_gruppen_names) == 1:
                    self._full_name = f"{self._wettkampf.name}_{self._gruppe.name}_{self.name}"
                else:
                    self._full_name = f"{self._wettkampf.name}_{self._interval_gruppen_names[0]}_to_{self._interval_gruppen_names[-1]}_{self.name}"
                self._num_athletes = 0
                for gruppen_name_inner in self._interval_gruppen_names:
                    self._num_athletes += self._teilnehmer_data[self._wettkampf.name][gruppen_name_inner]
            else:
                self._full_name = f"{self._wettkampf.name}_{gruppen_names[0]}_to_{gruppen_names[-1]}_{self.name}"
                self._num_athletes = 0
                for gruppen_name_inner in gruppen_names:
                    self._num_athletes += self._teilnehmer_data[self._wettkampf.name][gruppen_name_inner]
        else:
            self._full_name = f"{self._wettkampf.name}_{self._gruppe.name}_{self.name}"
            self._num_athletes = self._teilnehmer_data[self._wettkampf.name][self._gruppe.name]

    def evaluate_length(self, offset):
        gruppen_names = self._wettkampf.gruppen
        if not self.is_pause:
            if self.together and self.keep_groups_separate:
                disziplinen_length_calculated = 0
                for gruppen_name_inner in self._interval_gruppen_names:
                    disziplinen_length_calculated += self._get_calculated_disziplinen_length(wettkampf=self._wettkampf.name, disziplin=self.name, num_athletes=self._teilnehmer_data[self._wettkampf.name][gruppen_name_inner], exact=True)
                disziplinen_length_calculated = round(disziplinen_length_calculated, 3)
                logging.debug("offset: %s", offset)
                slot_begin = math.ceil(offset)
                logging.debug("slot_begin: %s", slot_begin)
                logging.debug("disziplinen_length_calculated: %s", disziplinen_length_calculated)
                self._length_calculated = disziplinen_length_calculated
                if self.is_first_gruppe_of_interval():
                    offset += round(disziplinen_length_calculated - slot_begin, 3)
                logging.debug("offset(new): %s", offset)
                disziplinen_length = math.ceil(offset)
                logging.debug("disziplinen_length: %s", disziplinen_length)
                if gruppen_names[-1] in self._interval_gruppen_names:
                    disziplinen_length += 1
                    logging.debug("disziplinen_length: %s", disziplinen_length)
                self._length = disziplinen_length
            else:
                disziplinen_length_calculated = self._get_calculated_disziplinen_length(wettkampf=self._wettkampf.name, disziplin=self.name, num_athletes=self._num_athletes)
                self._length_calculated = disziplinen_length_calculated
                if self.force_length:
                    disziplinen_length = self.length_data
                    self._length = disziplinen_length
                else:
                    disziplinen_length = disziplinen_length_calculated
                    self._length = disziplinen_length_calculated
                disziplinen_length += 1
                self._length = disziplinen_length
        else:
            disziplinen_length_calculated = None
            self._length_calculated = disziplinen_length_calculated
            disziplinen_length = self.length_data
            if not self._gruppe.disziplinen[-1].keep_groups_separate:
                disziplinen_length -= 1
        self._length_calculated = disziplinen_length_calculated
        self._length = disziplinen_length
        self._new_offset = offset

    def create_task_if_necessary(self):
        if self.length <= 0:
            return

        if not self.is_pause:
            logging.debug("      disziplin: %s (disziplin=%s, together=%s, athletes=%u, length_data=%u, length_calc=%u) => length+pause=%u", self.full_name, self.name, self.together, self.num_athletes, self.length_data, self.length_calculated, self.length)
        else:
            logging.debug("      disziplin: %s (length_data=%u) => length-pause=%u", self.full_name, self.length_data, self.length)

        try:
            self._task = self._scenario[self.full_name]
        except Exception:
            kwargs = {
                "name": self.full_name,
                "length": self.length,
                "length_data": self.length_data,
                "length_calc": self.length_calculated,
                "plot_color": self._wettkampf.plot_color,
                "together": self.together,
                "keep_groups_separate": self.keep_groups_separate,
            }
            self._task = self._scenario.Task(**kwargs)
        self._gruppe.disziplinen.append(self._task)

    @property
    def name(self):
        return self._definition["name"]

    @property
    def together(self):
        return self._definition.get("together", False)

    @property
    def length(self):
        return self._length

    @property
    def length_data(self):
        return self._definition["length"]

    @property
    def length_calculated(self):
        return self._length_calculated

    @property
    def force_length(self):
        return self._definition.get("force_length", False)

    @property
    def keep_groups_separate(self):
        return self._definition.get("keep_groups_separate", False)

    @property
    def use_num_anlagen(self):
        return self._definition.get("use_num_anlagen", 1)

    @property
    def resource(self):
        return self._definition.get("resource", None)

    @property
    def is_pause(self):
        return "pause" in self.name.lower()

    @property
    def full_name(self):
        return self._full_name

    @property
    def num_athletes(self):
        return self._num_athletes

    @property
    def interval_gruppen(self):
        return self._interval_gruppen_names

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        self._task = value

    @property
    def new_offset(self):
        return self._new_offset

    def _get_interval_gruppen(self, wettkampf_name, interesting_gruppen_name, gruppen_names, teilnehmer_data, item):
        logging.debug("      _get_interval_gruppen(wettkampf=%s, interesting=%s, gruppen=%s)...", wettkampf_name, interesting_gruppen_name, gruppen_names)
        current_interval = 0
        interval_gruppen = defaultdict(list)
        accumulated_disziplinen_length = 0
        for gruppen_name in gruppen_names:
            num_athletes = teilnehmer_data[wettkampf_name][gruppen_name]
            disziplinen_length = self._get_calculated_disziplinen_length(wettkampf=wettkampf_name, disziplin=item["name"], num_athletes=num_athletes, exact=True)
            accumulated_disziplinen_length += disziplinen_length
            logging.debug("accumulated_disziplinen_length: %s", round(accumulated_disziplinen_length, 3))
            if round(accumulated_disziplinen_length, 3) > current_interval + 1:
                current_interval += math.floor(round(accumulated_disziplinen_length, 3))
            interval_gruppen[current_interval].append(gruppen_name)
        for gruppen in interval_gruppen.values():
            if interesting_gruppen_name in gruppen:
                logging.debug("      _get_interval_gruppen(wettkampf=%s, interesting=%s, gruppen=%s) => %s", wettkampf_name, interesting_gruppen_name, gruppen_names, gruppen)
                return gruppen
        raise common.SomethingWentWrong("in _get_interval_gruppen()")

    def _get_calculated_disziplinen_length(self, wettkampf, disziplin, num_athletes, exact=False):
        mapping = {
            "60m": (6, 2/10),
            "80m": (6, 2/10),
            "100m": (6, 2/10),
            "100mHü": (6, 4/10),
            "110mHü": (6, 4/10),
            "200m": (6, 4/10),
            "400m": (6, 7/10),
            "800m": (6, 7/10),
            "600m": (16, 1),
            "1000m": (16, 1),
            "1500m": (16, 1),
            "Diskus": (1, 3/15),
            "Hoch": {
                "U14W_5K": (1, 3/15),
                "U14M_5K": (1, 3/15),
                "U16W_5K": (1, 5/15),
                "U16M_6K": (1, 5/15),
                "WOM_5K": (1, 3/15),
                "WOM_7K": (1, 5/15),
                "MAN_6K": (1, 3/15),
                "MAN_10K": (1, 5/15),
            },
            "Kugel": (1, 2/15),
            "Speer": (1, 3/15),
            "Stab": (1, 6/12),
            "Weit": (1, 3/15),
        }
        item = mapping[disziplin]
        if isinstance(item, dict):
            item = item[wettkampf]
        num_serien = ((num_athletes - 1) // item[0]) + 1
        calculated_length = num_serien * item[1]
        calculated_length = calculated_length / self.use_num_anlagen
        if not exact:
            calculated_length = math.ceil(calculated_length)
        logging.debug("      _get_calculated_disziplinen_length(wettkampf=%s, disziplin=%s, num_athletes=%s, num_anlagen=%s, exact=%s) => %s", wettkampf, disziplin, num_athletes, self.use_num_anlagen, exact, round(calculated_length, 3))
        return calculated_length
