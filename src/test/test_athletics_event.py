# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long
import logging
import unittest

import athletics_event
from .man_10k_event_data import event_data as man_10k_event_data_orig
from .man_6k_event_data import event_data as man_6k_event_data_orig
from .u12w_4k_event_data import event_data as u12w_4k_event_data_orig


logging.basicConfig(level=logging.WARNING)


class TestAthleticsEvent(unittest.TestCase):
    def test_instantiate_AthleticsEventScheduler(self):
        athletics_event.AthleticsEventScheduler(event_data=u12w_4k_event_data_orig, day="saturday", horizon=athletics_event.default_arguments["horizon"])

    def test_interactive_main_u12w_4k_event(self):
        athletics_event.interactive_main(u12w_4k_event_data_orig, ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(291, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_6k_event(self):
        athletics_event.interactive_main(man_6k_event_data_orig, ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(426, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_10k_event(self):
        athletics_event.interactive_main(man_10k_event_data_orig, ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(397, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(man_10k_event_data_orig, ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(589, athletics_event.event.scenario.objective_value())
