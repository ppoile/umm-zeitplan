"""Module providing Athletics Event implementation."""

import argparse
from collections import defaultdict
import datetime
import functools
import logging
import math
import operator
import os
import re

from pyschedule import Scenario, solvers, plotters
import zeitplan_xlsx_writer


# pylint: disable=missing-function-docstring,missing-class-docstring,line-too-long


def setup_logging(verbose, event_name):
    log_level = logging.INFO
    if verbose:
        log_level=logging.DEBUG
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f'{event_name}.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    root_logger.addHandler(ch)
    root_logger.addHandler(fh)
    matplotlib_logger = logging.getLogger("matplotlib")
    matplotlib_logger.setLevel(logging.INFO)
    zeitplan_logger = logging.getLogger("zeitplan")
    zeitplan_logger.setLevel(logging.INFO)


class SomethingWentWrong(RuntimeError):
    pass


class NoSolutionError(RuntimeError):
    pass


class AnlagenDescriptor():
    def __init__(self, name, size=1):
        self._name = name
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size


class AthleticsEventScheduler():
    def __init__(self, event_data, day, horizon):
        self._event_data = event_data
        self._day = day
        self._horizon = horizon
        self._anlagen = {}
        self._wettkampf_data = self._event_data['wettkampf_data'][self.day]
        self._teilnehmer_data = self._event_data['teilnehmer_data']
        self._last_disziplin = {}
        self._disziplinen = {}
        self._wettkampf_first_last_disziplinen = {}
        self._last_wettkampf_of_the_day = None
        self._hide_tasks = []
        self.create_scenario()

    def create_scenario(self):
        self._scenario = Scenario(name=self.short_name, horizon=self.horizon)

    @property
    def short_name(self):
        return self._event_data['event_name_short']

    @property
    def day(self):
        return self._day

    @property
    def horizon(self):
        return self._horizon

    @property
    def scenario(self):
        return self._scenario

    @property
    def anlagen(self):
        return self._anlagen

    def create_anlagen(self):
        logging.debug('creating anlagen...')
        for descriptor in self._event_data['anlagen_descriptors'][self.day]:
            self._create_anlage(descriptor)

    def _create_anlage(self, descriptor_args):
        descriptor = AnlagenDescriptor(*descriptor_args)
        for i in range(descriptor.size):
            anlagen_name = descriptor.name
            if descriptor.size > 1:
                anlagen_name += "{}".format(i + 1)
            logging.debug("  %s", anlagen_name)
            anlage = self._scenario.Resource(anlagen_name)
            self._anlagen[anlagen_name] = anlage

    def _any_anlage(self, pattern):
        return functools.reduce(lambda a, b: operator.or_(a, b), self._get_all_anlagen(pattern))

    def _get_all_anlagen(self, pattern):
        resources = []
        for anlagen_name, anlage in self._anlagen.items():
            if anlagen_name.startswith(pattern):
                resources.append(anlage)
        return resources

    @property
    def disziplinen(self):
        return self._disziplinen

    def create_disziplinen(self):
        logging.debug('creating disziplinen...')
        for wettkampf_name in self._wettkampf_data:
            if wettkampf_name not in self._teilnehmer_data:
                continue
            logging.debug("  wettkampf: %s", wettkampf_name)
            keep_groups_separate_disziplinen = []
            is_wettkampf_with_strict_sequence = self._wettkampf_data[wettkampf_name].get("is_wettkampf_with_strict_sequence", False)
            if self._wettkampf_data[wettkampf_name].get("is_last_wettkampf_of_the_day", False):
                self._last_wettkampf_of_the_day = wettkampf_name
            gruppen_names = list(self._teilnehmer_data[wettkampf_name].keys())
            wettkampf_gruppen_first_and_last_disziplinen = []
            wettkampf_disziplinen_factors = defaultdict(int)
            offset = 0
            for gruppen_name in gruppen_names:
                logging.debug("    gruppe: %s", gruppen_name)
                gruppe = self._scenario.Resource(gruppen_name)
                gruppen_disziplinen = []
                for disziplinen_data in self._wettkampf_data[wettkampf_name]["disziplinen"]:
                    together = disziplinen_data.get("together", False)
                    force_length = disziplinen_data.get("force_length", False)
                    keep_groups_separate = disziplinen_data.get("keep_groups_separate", False)
                    num_anlagen = disziplinen_data.get("use_num_anlagen", 1)
                    if together:
                        if keep_groups_separate:
                            interval_gruppen_names = self._get_interval_gruppen(wettkampf_name, gruppen_name, gruppen_names, self._teilnehmer_data, disziplinen_data, num_anlagen)
                            if len(interval_gruppen_names) == 1:
                                disziplinen_name = f"{wettkampf_name}_{gruppen_name}_{disziplinen_data['name']}"
                            else:
                                disziplinen_name = f"{wettkampf_name}_{interval_gruppen_names[0]}_to_{interval_gruppen_names[-1]}_{disziplinen_data['name']}"
                            num_athletes = 0
                            for gruppen_name_inner in interval_gruppen_names:
                                num_athletes += self._teilnehmer_data[wettkampf_name][gruppen_name_inner]
                        else:
                            disziplinen_name = f"{wettkampf_name}_{gruppen_names[0]}_to_{gruppen_names[-1]}_{disziplinen_data['name']}"
                            num_athletes = 0
                            for gruppen_name_inner in gruppen_names:
                                num_athletes += self._teilnehmer_data[wettkampf_name][gruppen_name_inner]
                    else:
                        disziplinen_name = f"{wettkampf_name}_{gruppen_name}_{disziplinen_data['name']}"
                        num_athletes = self._teilnehmer_data[wettkampf_name][gruppen_name]
                    if disziplinen_name not in self._disziplinen.keys():  # pylint: disable=consider-iterating-dictionary
                        disziplinen_length_data = disziplinen_data["length"]
                        if "pause" not in disziplinen_name.lower():
                            if together and keep_groups_separate:
                                disziplinen_length_calculated = 0
                                for gruppen_name_inner in interval_gruppen_names:
                                    disziplinen_length_calculated += self._get_calculated_disziplinen_length(wettkampf=wettkampf_name, disziplin=disziplinen_data["name"], num_athletes=self._teilnehmer_data[wettkampf_name][gruppen_name_inner], num_anlagen=num_anlagen, exact=True)
                                logging.debug("offset: %s", offset)
                                slot_begin = math.ceil(offset)
                                logging.debug("slot_begin: %s", slot_begin)
                                logging.debug("disziplinen_length_calculated: %s", disziplinen_length_calculated)
                                offset = offset - slot_begin + disziplinen_length_calculated
                                logging.debug("offset(new): %s", offset)
                                disziplinen_length = math.ceil(round(offset, 3))
                                logging.debug("disziplinen_length: %s", disziplinen_length)
                                if gruppen_names[-1] in interval_gruppen_names:
                                    disziplinen_length += 1
                                    logging.debug("disziplinen_length: %s", disziplinen_length)
                            else:
                                disziplinen_length_calculated = self._get_calculated_disziplinen_length(wettkampf=wettkampf_name, disziplin=disziplinen_data["name"], num_athletes=num_athletes, num_anlagen=num_anlagen)
                                if force_length:
                                    disziplinen_length = disziplinen_length_data
                                else:
                                    disziplinen_length = disziplinen_length_calculated
                                disziplinen_length += 1
                        else:
                            disziplinen_length_calculated = None
                            disziplinen_length = disziplinen_length_data
                            if not gruppen_disziplinen[-1].keep_groups_separate:
                                disziplinen_length -= 1
                                if disziplinen_length <= 0:
                                    continue
                        kwargs = {
                            "name": disziplinen_name,
                            "length": disziplinen_length,
                            "length_data": disziplinen_length_data,
                            "length_calc": disziplinen_length_calculated,
                            "plot_color": self._wettkampf_data[wettkampf_name]["plot_color"],
                            "together": together,
                            "keep_groups_separate": keep_groups_separate,
                        }
                        disziplinen_task = self._scenario.Task(**kwargs)
                        self._disziplinen[disziplinen_name] = disziplinen_task
                    else:
                        disziplinen_task = self._disziplinen[disziplinen_name]
                        disziplinen_length = disziplinen_task.length
                        disziplinen_length_data = disziplinen_task.length_data
                        disziplinen_length_calculated = disziplinen_task.length_calc
                    if "pause" not in disziplinen_name.lower():
                        logging.debug("      disziplin: %s (disziplin=%s, together=%s, athletes=%u, length_data=%u, length_calc=%u) => length+pause=%u", disziplinen_name, disziplinen_data["name"], together, num_athletes, disziplinen_length_data, disziplinen_length_calculated, disziplinen_length)
                    else:
                        logging.debug("      disziplin: %s (length_data=%u) => length-pause=%u", disziplinen_name, disziplinen_length_data, disziplinen_length)
                    gruppen_disziplinen.append(disziplinen_task)

                    resource = disziplinen_data.get("resource", None)
                    if resource:
                        if not together or gruppen_name == gruppen_names[0] or keep_groups_separate and (gruppen_name == interval_gruppen_names[0]):
                            for resource_name in resource.split("&"):
                                disziplinen_task += self._any_anlage(resource_name)

                    disziplinen_task += gruppe

                    if together and keep_groups_separate and disziplinen_task not in keep_groups_separate_disziplinen:
                        keep_groups_separate_disziplinen.append(disziplinen_task)

                    if "pause" in disziplinen_name.lower():
                        self._hide_tasks.append(disziplinen_task)

                wettkampf_gruppen_first_and_last_disziplinen.append((gruppen_disziplinen[0], gruppen_disziplinen[-1]))
                self._add_gruppen_disziplinen_dependencies(gruppen_disziplinen, is_wettkampf_with_strict_sequence)
                self._update_wettampf_disziplinen_factors(gruppen_disziplinen, wettkampf_disziplinen_factors)

            for item_index in range(1, len(keep_groups_separate_disziplinen)):
                self._scenario += keep_groups_separate_disziplinen[item_index - 1] <= keep_groups_separate_disziplinen[item_index]

            wettkampf_first_disziplin = wettkampf_gruppen_first_and_last_disziplinen[0][0]
            wettkampf_last_disziplin = wettkampf_gruppen_first_and_last_disziplinen[-1][-1]
            self._wettkampf_first_last_disziplinen[wettkampf_name] = (wettkampf_first_disziplin, wettkampf_last_disziplin)
            self._set_default_objective(wettkampf_disziplinen_factors, wettkampf_first_disziplin, wettkampf_last_disziplin)
            self._last_disziplin[wettkampf_name] = wettkampf_last_disziplin

    def _get_interval_gruppen(self, wettkampf_name, interesting_gruppen_name, gruppen_names, teilnehmer_data, item, num_anlagen):
        logging.debug("      _get_interval_gruppen(wettkampf=%s, interesting=%s, gruppen=%s)...", wettkampf_name, interesting_gruppen_name, gruppen_names)
        current_interval = 0
        interval_gruppen = defaultdict(list)
        accumulated_disziplinen_length = 0
        for gruppen_name in gruppen_names:
            num_athletes = teilnehmer_data[wettkampf_name][gruppen_name]
            disziplinen_length = self._get_calculated_disziplinen_length(wettkampf=wettkampf_name, disziplin=item["name"], num_athletes=num_athletes, num_anlagen=num_anlagen, exact=True)
            accumulated_disziplinen_length += disziplinen_length
            logging.debug("accumulated_disziplinen_length: %s", accumulated_disziplinen_length)
            if round(accumulated_disziplinen_length, 3) > current_interval + 1:
                current_interval += math.floor(round(accumulated_disziplinen_length, 3))
            interval_gruppen[current_interval].append(gruppen_name)
        for gruppen in interval_gruppen.values():
            if interesting_gruppen_name in gruppen:
                logging.debug("      _get_interval_gruppen(wettkampf=%s, interesting=%s, gruppen=%s) => %s", wettkampf_name, interesting_gruppen_name, gruppen_names, gruppen)
                return gruppen
        raise SomethingWentWrong("in _get_interval_gruppen()")

    def _get_disziplinen_without_pausen(self, disziplinen):
        disziplinen_without_pausen = []
        for disziplin in disziplinen:
            if "pause" not in disziplin["name"].lower():
                disziplinen_without_pausen.append(disziplin)
        return disziplinen_without_pausen

    def _get_calculated_disziplinen_length(self, wettkampf, disziplin, num_athletes, num_anlagen, exact=False):
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
        calculated_length = calculated_length / num_anlagen
        if not exact:
            calculated_length = math.ceil(calculated_length)
        logging.debug("      _get_calculated_disziplinen_length(wettkampf=%s, disziplin=%s, num_athletes=%s, num_anlagen=%s, exact=%s) => %s", wettkampf, disziplin, num_athletes, num_anlagen, exact, calculated_length)
        return calculated_length

    def _add_gruppen_disziplinen_dependencies(self, gruppen_disziplinen, is_wettkampf_with_strict_sequence):
        first_disziplin = gruppen_disziplinen[0]
        last_disziplin = gruppen_disziplinen[-1]
        gruppen_disziplinen_without_pausen = self._get_disziplinen_without_pausen(gruppen_disziplinen)
        if is_wettkampf_with_strict_sequence:
            # one after another: 1st, 1st-pause, 2nd, 2nd-pause, 3rd,...
            current_disziplin = gruppen_disziplinen[0]
            for next_disziplin in gruppen_disziplinen[1:]:
                self._scenario += current_disziplin < next_disziplin
                current_disziplin = next_disziplin
        else:
            # 1st and last set - rest free
            wettkampf_with_all_pausen = len(gruppen_disziplinen) == 2 * len(gruppen_disziplinen_without_pausen) - 1
            wettkampf_with_first_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 1) and "pause" in gruppen_disziplinen[1]["name"].lower()
            wettkampf_with_last_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 1) and "pause" in gruppen_disziplinen[-2]["name"].lower()
            wettkampf_with_first_and_last_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 2) and "pause" in gruppen_disziplinen[1]["name"].lower() and "pause" in gruppen_disziplinen[-2]["name"].lower()
            wettkampf_with_no_pause = len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen)

            if wettkampf_with_all_pausen:
                # with all pausen
                for disziplin_index in range(len(gruppen_disziplinen[:-1:2])):
                    self._scenario += gruppen_disziplinen[disziplin_index * 2] <= gruppen_disziplinen[disziplin_index * 2 + 1]
                first_pause = gruppen_disziplinen[1]
                for disziplin in gruppen_disziplinen[2::2]:
                    self._scenario += first_pause < disziplin
                for disziplin in gruppen_disziplinen[1::2]:
                    self._scenario += disziplin < last_disziplin
            elif wettkampf_with_last_pause:
                # with last pause
                first_disziplin = gruppen_disziplinen_without_pausen[0]
                for disziplin in gruppen_disziplinen[1:-1]:
                    self._scenario += first_disziplin < disziplin
                last_pause = gruppen_disziplinen[-2]
                self._scenario += last_pause <= gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[:-2]:
                    self._scenario += disziplin < last_pause
            elif wettkampf_with_first_and_last_pause:
                # with first and last pause
                first_pause = gruppen_disziplinen[1]
                self._scenario += gruppen_disziplinen[0] <= first_pause
                for disziplin in gruppen_disziplinen[2:-2]:
                    self._scenario += first_pause < disziplin
                last_pause = gruppen_disziplinen[-2]
                self._scenario += last_pause <= gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[2:-2]:
                    self._scenario += disziplin < last_pause
            elif wettkampf_with_first_pause:
                # with first pause
                first_pause = gruppen_disziplinen[1]
                self._scenario += gruppen_disziplinen[0] <= first_pause
                for disziplin in gruppen_disziplinen[2:-1]:
                    self._scenario += first_pause < disziplin
                last_disziplin = gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[2:-1]:
                    self._scenario += disziplin < last_disziplin
            elif wettkampf_with_no_pause:
                # with no pause
                for disziplin in gruppen_disziplinen[1:]:
                    self._scenario += first_disziplin < disziplin
                for disziplin in gruppen_disziplinen[:-1]:
                    self._scenario += disziplin < last_disziplin
            else:
                raise ValueError()

    def _update_wettampf_disziplinen_factors(self, gruppen_disziplinen, wettkampf_disziplinen_factors):
        for disziplin in self._get_disziplinen_without_pausen(gruppen_disziplinen)[1:]:
            wettkampf_disziplinen_factors[disziplin['name']] += 1
        wettkampf_disziplinen_factors[disziplin['name']] += 1

    def _set_default_objective(self, wettkampf_disziplinen_factors, first_disziplin, last_disziplin):
        for disziplin_name, factor in wettkampf_disziplinen_factors.items():
            disziplin = self._disziplinen[disziplin_name]
            self._scenario += disziplin * factor
        factor_sum = sum([factor for factor in wettkampf_disziplinen_factors.values()])
        self._scenario += first_disziplin * -(factor_sum - 1)

    def get_disziplin_from_name(self, disziplinen_name_or_pattern):
        for candidate, disziplin in self._disziplinen.items():
            match = re.match(disziplinen_name_or_pattern, candidate)
            if match is not None:
                return disziplin
        return self._disziplinen[disziplinen_name_or_pattern]

    def set_wettkampf_start_times(self, wettkampf_start_times):
        logging.debug('setting wettkampf start times...')
        for disziplinen_name_or_pattern, start_times in wettkampf_start_times.items():
            disziplin = self.get_disziplin_from_name(disziplinen_name_or_pattern)
            self._scenario += disziplin > start_times

    def set_objective(self, disziplinen_factors):
        self._scenario.clear_objective()
        for disziplin_name, factor in disziplinen_factors.items():
            self._scenario += self._disziplinen[disziplin_name] * factor

    def ensure_last_wettkampf_of_the_day(self):
        if self._last_wettkampf_of_the_day is None:
            return
        logging.debug('ensuring last wettkampf of the day...')
        last_disziplin_of_the_day = self._last_disziplin[self._last_wettkampf_of_the_day]
        for wettkampf_name, last_disziplin in self._last_disziplin.items():
            if wettkampf_name != self._last_wettkampf_of_the_day:
                self._scenario += last_disziplin < last_disziplin_of_the_day
        self._scenario += last_disziplin_of_the_day * 10

    def get_groups(self, wettkampf_name):
        return list(self._teilnehmer_data[wettkampf_name].keys())

    def get_disziplinen(self, wettkampf_name):
        return list(self._wettkampf_data[wettkampf_name]["disziplinen"])

    def get_wettkampf_duration_summary(self):
        heading = "Wettkampf-Duration-Summary:"
        lines = []
        wettkampf_duration_sum = 0
        event_first_disziplin = 999999
        event_last_disziplin = 0
        for wettkampf_name, (first_disziplin, last_disziplin) in self._wettkampf_first_last_disziplinen.items():
            if event_first_disziplin is None or first_disziplin.start_value < event_first_disziplin:
                event_first_disziplin = first_disziplin.start_value
            if event_last_disziplin is None or last_disziplin.start_value > event_last_disziplin:
                event_last_disziplin = last_disziplin.start_value
            lines.append(f"  {wettkampf_name}: {first_disziplin.start_value}..{last_disziplin.start_value} ({last_disziplin.start_value - first_disziplin.start_value})")
            wettkampf_duration_sum += last_disziplin.start_value - first_disziplin.start_value
        lines.append(f"horizon: {event_last_disziplin - event_first_disziplin + 1}")
        lines.append(f"cumulated-wettkampf-duration: {wettkampf_duration_sum}")
        return "{}\n{}".format(heading, "\n".join(lines))

    def solve(self, time_limit, event_name, event_day, ratio_gap=0.0, random_seed=None, threads=None, msg=1):
        logging.debug('solving problem with mip solver...')
        status = solvers.mip.solve(self._scenario, time_limit=time_limit, ratio_gap=ratio_gap, random_seed=random_seed, threads=threads, msg=msg)
        cbc_logfile_name = "cbc.log"
        if os.path.exists(cbc_logfile_name):
            with open(cbc_logfile_name, encoding="utf-8") as cbc_logfile:
                logging.info(cbc_logfile.read())
        else:
            logging.info("no '%s' found", cbc_logfile_name)
        if not status:
            raise NoSolutionError()

        solution_as_string = str(self._scenario.solution())
        solution_filename = f"{self.short_name}_solution.txt"
        with open(solution_filename, 'w', encoding="utf-8") as f:
            f.write(solution_as_string)
        logging.info(solution_as_string)
        plotters.matplotlib.plot(self._scenario, show_task_labels=True, img_filename=f"{self.short_name}.png",
                                 fig_size=(100, 5), hide_tasks=self._hide_tasks)
        with open(solution_filename, 'r', encoding="utf-8") as solution_file:
            zeitplan_xlsx_writer.main(solution_file, event_name=event_name, event_day=event_day.title(), start_time="9:00")
        logging.info(self.get_wettkampf_duration_summary())
        logging.info("objective_value: %s", self._scenario.objective_value())


event = None  # pylint: disable=invalid-name


def main(event_data, args):
    start_time = datetime.datetime.now()
    event_name_short = event_data['event_name_short']
    output_folder_name = f"{start_time.isoformat(timespec='seconds')}_{event_name_short}_{args.day}_{args.horizon}_{args.time_limit}"
    if args.ratio_gap != default_arguments["ratio_gap"]:
        ratio_gap_as_string = str(args.ratio_gap)
        gap_suffix = ratio_gap_as_string.replace('.', 'g')
        output_folder_name += "_" + gap_suffix
    results_folder_path = os.path.join(os.path.dirname(__file__), os.pardir, "results")
    output_folder_path = os.path.join(results_folder_path, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)
    link_path = os.path.join(results_folder_path, "latest")
    if os.path.lexists(link_path):
        os.remove(link_path)
    os.symlink(output_folder_name, link_path)
    os.chdir(output_folder_path)

    setup_logging(args.verbose, event_name_short)

    logging.debug("arguments: %s", args)
    logging.debug("output folder: %r", output_folder_name)

    global event  # pylint: disable=global-statement
    event = AthleticsEventScheduler(
        event_data=event_data, day=args.day, horizon=args.horizon)
    event.create_anlagen()
    event.create_disziplinen()
    if not args.dont_set_start_time:
        event.set_wettkampf_start_times(event_data['wettkampf_start_times'][args.day])
    event.ensure_last_wettkampf_of_the_day()
    scenario_as_string = str(event.scenario)
    scenario_filename = f"{event_name_short}_scenario.txt"
    with open(scenario_filename, 'w', encoding="utf-8") as f:
        f.write(scenario_as_string)
    if args.print_scenario_and_exit:
        logging.info("scenario: %s", scenario_as_string)
        return 0
    logging.debug("scenario: %s", scenario_as_string)

    time_limit_in_secs = get_time_limit_in_secs_from_argument_string(args.time_limit)

    try:
        event.solve(
            time_limit=time_limit_in_secs,
            ratio_gap=args.ratio_gap,
            random_seed=args.random_seed,
            threads=args.threads,
            event_name=event_data['event_name'],
            event_day=args.day)
    except NoSolutionError as e:
        logging.error("Exception caught: %s", e.__class__.__name__)
        return -1
    logging.info("output folder: %r", output_folder_name)
    logging.debug("done")
    return 0


def get_time_limit_in_secs_from_argument_string(time_limit_as_string):
    if time_limit_as_string.endswith('s'):
        time_limit_in_secs = float(time_limit_as_string[:-1])
    elif time_limit_as_string.endswith('m'):
        time_limit_in_secs = float(time_limit_as_string[:-1]) * 60
    elif time_limit_as_string.endswith('h'):
        time_limit_in_secs = float(time_limit_as_string[:-1]) * 3600
    else:
        time_limit_in_secs = float(time_limit_as_string)
    return time_limit_in_secs


default_arguments = {
    "time_limit": "10m",
    "ratio_gap": 0.0,
    "random_seed": None,
    "threads": None,
    "horizon": 54,
}


def interactive_main(event_data, arguments=None):
    parser = argparse.ArgumentParser(description='calculate event timetable')
    parser.add_argument('--print-scenario-and-exit', action="store_true",
                        help='print scenario and exit')
    parser.add_argument('-v', '--verbose', action="store_true", help="be verbose")
    help_text = f'time limit, e.g. 30s, 10m, 1h (default: {default_arguments["time_limit"]})'
    parser.add_argument('--time-limit', default=default_arguments["time_limit"], help=help_text)
    help_text = f'ratio gap, e.g. 0.3 (default: {default_arguments["ratio_gap"]})'
    parser.add_argument('--ratio-gap', type=float, default=default_arguments["ratio_gap"], help=help_text)
    help_text = f'random seed, e.g. 42 (default: {default_arguments["random_seed"]})'
    parser.add_argument('--random-seed', type=int, default=default_arguments["random_seed"], help=help_text)
    help_text = f'threads, e.g. 4 (default: {default_arguments["threads"]})'
    parser.add_argument('--threads', type=int, default=default_arguments["threads"], help=help_text)
    parser.add_argument('--dont-set-start-time', action="store_true", help="don't set start time")
    help_text = f'horizon, (default: {default_arguments["horizon"]})'
    parser.add_argument('--horizon', type=int, default=default_arguments["horizon"], help=help_text)
    valid_wettkampf_days = event_data['wettkampf_data'].keys()
    parser.add_argument('day', type=str.lower, choices=valid_wettkampf_days, help='wettkampf day')
    parsed_arguments = parser.parse_args(arguments)

    return main(event_data, parsed_arguments)
