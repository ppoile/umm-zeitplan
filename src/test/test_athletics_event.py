# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long
from copy import deepcopy
import logging
import unittest

import athletics_event
from .event_data import generate_event_data


logging.basicConfig(level=logging.WARNING)


class TestAthleticsEvent(unittest.TestCase):
    def test_instantiate_AthleticsEventScheduler(self):
        athletics_event.AthleticsEventScheduler(event_data=generate_event_data("U12W_4K"), day="saturday", horizon=athletics_event.default_arguments["horizon"])

    def test_interactive_main_u12w_4k_event(self):
        athletics_event.interactive_main(generate_event_data("U12W_4K"), ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(291, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_6k_event(self):
        athletics_event.interactive_main(generate_event_data("MAN_6K"), ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(426, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_10k_event(self):
        man_10k_event_data = generate_event_data("MAN_10K")
        athletics_event.interactive_main(man_10k_event_data, ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(397, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(man_10k_event_data, ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(589, athletics_event.event.scenario.objective_value())
