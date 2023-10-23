"""Module providing Athletics Event implementation."""

# pylint: disable=missing-function-docstring,missing-class-docstring,line-too-long

import argparse
from collections import defaultdict
import datetime
import logging
import math
import os
import re

from pyschedule import Scenario, solvers, plotters

from . import common
from .disziplin import Disziplin
from .gruppe import Gruppe
from .wettkampf import Wettkampf
from . import zeitplan_xlsx_writer


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
                anlagen_name += f"{i + 1}"
            logging.debug("  %s", anlagen_name)
            anlage = self._scenario.Resource(anlagen_name)
            self._anlagen[anlagen_name] = anlage

    def create_disziplinen(self):
        logging.debug('creating disziplinen...')
        for wettkampf_name in self._wettkampf_data:
            self._process_wettkampf(wettkampf_name)

    def _process_wettkampf(self, wettkampf_name):
        if wettkampf_name not in self._teilnehmer_data:
            return

        wettkampf = Wettkampf(wettkampf_name, self._wettkampf_data, self._teilnehmer_data)
        keep_groups_separate_disziplinen = []
        if wettkampf.is_last_wettkampf_of_the_day:
            self._last_wettkampf_of_the_day = wettkampf.name
        wettkampf_gruppen_first_and_last_disziplinen = []
        wettkampf_disziplinen_factors = defaultdict(int)
        offset = 0
        for gruppen_name in wettkampf.gruppen:
            gruppe = Gruppe(gruppen_name, self._scenario)
            for disziplinen_data in wettkampf.disziplinen_data:
                disziplin = Disziplin(disziplinen_data, wettkampf, gruppe, self._wettkampf_data, self._teilnehmer_data, self.scenario, self._anlagen, offset)
                if disziplin.length <= 0:
                    continue
                offset = disziplin.new_offset
                disziplin.assign_anlagen()
                disziplin.task += gruppe.resource

                if disziplin.together and disziplin.keep_groups_separate and disziplin.task not in keep_groups_separate_disziplinen:
                    keep_groups_separate_disziplinen.append(disziplin.task)

                if disziplin.is_pause:
                    self._hide_tasks.append(disziplin.task)

            wettkampf_gruppen_first_and_last_disziplinen.append((gruppe.disziplinen[0], gruppe.disziplinen[-1]))
            self._add_gruppen_disziplinen_dependencies(gruppe.disziplinen, wettkampf.is_wettkampf_with_strict_sequence)
            self._update_wettampf_disziplinen_factors(gruppe.disziplinen, wettkampf_disziplinen_factors)

        for item_index in range(1, len(keep_groups_separate_disziplinen)):
            self._scenario += keep_groups_separate_disziplinen[item_index - 1] <= keep_groups_separate_disziplinen[item_index]

        wettkampf_first_disziplin = wettkampf_gruppen_first_and_last_disziplinen[0][0]
        wettkampf_last_disziplin = wettkampf_gruppen_first_and_last_disziplinen[-1][-1]
        self._wettkampf_first_last_disziplinen[wettkampf.name] = (wettkampf_first_disziplin, wettkampf_last_disziplin)
        self._set_default_objective(wettkampf_disziplinen_factors, wettkampf_first_disziplin, wettkampf_last_disziplin)
        self._last_disziplin[wettkampf.name] = wettkampf_last_disziplin

    def _add_gruppen_disziplinen_dependencies(self, gruppen_disziplinen, is_wettkampf_with_strict_sequence):
        logging.debug("_add_gruppen_disziplinen_dependencies()...")
        first_disziplin = gruppen_disziplinen[0]
        last_disziplin = gruppen_disziplinen[-1]
        gruppen_disziplinen_without_pausen = self._get_disziplinen_without_pausen(gruppen_disziplinen)
        if is_wettkampf_with_strict_sequence:
            logging.debug("is_wettkampf_with_strict_sequence")
            logging.debug("one after another: 1st, 1st-pause, 2nd, 2nd-pause, 3rd,...")
            current_disziplin = gruppen_disziplinen[0]
            for next_disziplin in gruppen_disziplinen[1:]:
                self._scenario += current_disziplin < next_disziplin
                current_disziplin = next_disziplin
        else:
            logging.debug("not is_wettkampf_with_strict_sequence")
            logging.debug("1st and last set - rest free")
            wettkampf_with_all_pausen = len(gruppen_disziplinen) == 2 * len(gruppen_disziplinen_without_pausen) - 1
            wettkampf_with_first_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 1) and "pause" in gruppen_disziplinen[1]["name"].lower()
            wettkampf_with_last_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 1) and "pause" in gruppen_disziplinen[-2]["name"].lower()
            wettkampf_with_first_and_last_pause = (len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen) + 2) and "pause" in gruppen_disziplinen[1]["name"].lower() and "pause" in gruppen_disziplinen[-2]["name"].lower()
            wettkampf_with_no_pause = len(gruppen_disziplinen) == len(gruppen_disziplinen_without_pausen)

            if wettkampf_with_all_pausen:
                logging.debug("with all pausen")
                for disziplin_index in range(len(gruppen_disziplinen[:-1:2])):
                    self._scenario += gruppen_disziplinen[disziplin_index * 2] <= gruppen_disziplinen[disziplin_index * 2 + 1]
                first_pause = gruppen_disziplinen[1]
                for disziplin in gruppen_disziplinen[2::2]:
                    self._scenario += first_pause < disziplin
                for disziplin in gruppen_disziplinen[1::2]:
                    self._scenario += disziplin < last_disziplin
            elif wettkampf_with_last_pause:
                logging.debug("with last pause")
                first_disziplin = gruppen_disziplinen_without_pausen[0]
                for disziplin in gruppen_disziplinen[1:-1]:
                    self._scenario += first_disziplin < disziplin
                last_pause = gruppen_disziplinen[-2]
                self._scenario += last_pause <= gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[:-2]:
                    self._scenario += disziplin < last_pause
            elif wettkampf_with_first_and_last_pause:
                logging.debug("with first and last pause")
                first_pause = gruppen_disziplinen[1]
                self._scenario += gruppen_disziplinen[0] <= first_pause
                for disziplin in gruppen_disziplinen[2:-2]:
                    self._scenario += first_pause < disziplin
                last_pause = gruppen_disziplinen[-2]
                self._scenario += last_pause <= gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[2:-2]:
                    self._scenario += disziplin < last_pause
            elif wettkampf_with_first_pause:
                logging.debug("with first pause")
                first_pause = gruppen_disziplinen[1]
                self._scenario += gruppen_disziplinen[0] <= first_pause
                for disziplin in gruppen_disziplinen[2:-1]:
                    self._scenario += first_pause < disziplin
                last_disziplin = gruppen_disziplinen[-1]
                for disziplin in gruppen_disziplinen[2:-1]:
                    self._scenario += disziplin < last_disziplin
            elif wettkampf_with_no_pause:
                logging.debug("with no pause")
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

    def _get_disziplinen_without_pausen(self, disziplinen):
        disziplinen_without_pausen = []
        for disziplin in disziplinen:
            if "pause" not in disziplin["name"].lower():
                disziplinen_without_pausen.append(disziplin)
        return disziplinen_without_pausen

    def _set_default_objective(self, wettkampf_disziplinen_factors, first_disziplin, last_disziplin):
        for disziplin_name, factor in wettkampf_disziplinen_factors.items():
            disziplin = self._scenario[disziplin_name]
            self._scenario += disziplin * factor
        factor_sum = sum([factor for factor in wettkampf_disziplinen_factors.values()])
        self._scenario += first_disziplin * -(factor_sum - 1)

    def set_wettkampf_start_times(self, wettkampf_start_times):
        logging.debug('setting wettkampf start times...')
        for disziplinen_name_or_pattern, start_times in wettkampf_start_times.items():
            disziplin = self._get_disziplin_from_name(disziplinen_name_or_pattern)
            self._scenario += disziplin > start_times

    def _get_disziplin_from_name(self, disziplinen_name_or_pattern):
        for candidate in self._scenario.tasks():
            match = re.match(disziplinen_name_or_pattern, candidate.name)
            if match is not None:
                return candidate
        return self._scenario[disziplinen_name_or_pattern]

    def ensure_last_wettkampf_of_the_day(self):
        if self._last_wettkampf_of_the_day is None:
            return
        logging.debug('ensuring last wettkampf of the day...')
        last_disziplin_of_the_day = self._last_disziplin[self._last_wettkampf_of_the_day]
        for wettkampf_name, last_disziplin in self._last_disziplin.items():
            if wettkampf_name != self._last_wettkampf_of_the_day:
                self._scenario += last_disziplin < last_disziplin_of_the_day
        self._scenario += last_disziplin_of_the_day * 10

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
            raise common.NoSolutionError()

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


event = None  # pylint: disable=invalid-name


def main(event_data, args):
    start_time = datetime.datetime.now()
    event_name_short = event_data['event_name_short']
    output_folder_name = f"{start_time.isoformat(timespec='seconds')}_{event_name_short}_{args.day}_{args.horizon}_{args.time_limit}"
    if args.ratio_gap != default_arguments["ratio_gap"]:
        ratio_gap_as_string = str(args.ratio_gap)
        gap_suffix = ratio_gap_as_string.replace('.', 'g')
        output_folder_name += "_" + gap_suffix
    results_folder_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "results")
    output_folder_path = os.path.join(results_folder_path, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)
    link_path = os.path.join(results_folder_path, "latest")
    if os.path.lexists(link_path):
        os.remove(link_path)
    os.symlink(output_folder_name, link_path)
    os.chdir(output_folder_path)

    common.setup_logging(args.verbose, event_name_short)

    logging.debug("arguments: %s", args)
    logging.debug("output folder: %r", output_folder_name)

    global event  # pylint: disable=global-statement
    event = AthleticsEventScheduler(
        event_data=event_data, day=args.day, horizon=args.horizon)
    event.create_anlagen()
    event.create_disziplinen()
    if args.set_start_time:
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
            event_day=args.day,
            msg=args.verbose)
    except common.NoSolutionError as e:
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
    parser.add_argument('-s', '--silent', action="store_false", dest='verbose', help="be silent")
    help_text = f'time limit, e.g. 30s, 10m, 1h (default: {default_arguments["time_limit"]})'
    parser.add_argument('--time-limit', default=default_arguments["time_limit"], help=help_text)
    help_text = f'ratio gap, e.g. 0.3 (default: {default_arguments["ratio_gap"]})'
    parser.add_argument('--ratio-gap', type=float, default=default_arguments["ratio_gap"], help=help_text)
    help_text = f'random seed, e.g. 42 (default: {default_arguments["random_seed"]})'
    parser.add_argument('--random-seed', type=int, default=default_arguments["random_seed"], help=help_text)
    help_text = f'threads, e.g. 4 (default: {default_arguments["threads"]})'
    parser.add_argument('--threads', type=int, default=default_arguments["threads"], help=help_text)
    parser.add_argument('--dont-set-start-time', action="store_false", dest='set_start_time', help="don't set start time")
    help_text = f'horizon, (default: {default_arguments["horizon"]})'
    parser.add_argument('--horizon', type=int, default=default_arguments["horizon"], help=help_text)
    valid_wettkampf_days = event_data['wettkampf_data'].keys()
    parser.add_argument('day', type=str.lower, choices=valid_wettkampf_days, help='wettkampf day')
    parsed_arguments = parser.parse_args(arguments)

    return main(event_data, parsed_arguments)
