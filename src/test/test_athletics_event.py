# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long
from copy import deepcopy
import logging
import unittest

import athletics_event
from .event_data import generate_single_event_data


logging.basicConfig(level=logging.WARNING)


class TestAthleticsEvent(unittest.TestCase):
    def test_instantiate_AthleticsEventScheduler(self):
        athletics_event.AthleticsEventScheduler(event_data=generate_single_event_data("U12W_4K"), day="saturday", horizon=athletics_event.default_arguments["horizon"])

    def no_test_interactive_main_u12m_4k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U12M_4K"), ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(221, athletics_event.event.scenario.objective_value())

    def test_interactive_main_u12w_4k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U12W_4K"), ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(291, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_u14m_5k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U14M_5K"), ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(312, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_u14w_5k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U14W_5K"), ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(844, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_u16_6k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U16M_6K"), ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(416, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_u16w_5k_event(self):
        athletics_event.interactive_main(generate_single_event_data("U16W_5K"), ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(335, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_6k_event(self):
        athletics_event.interactive_main(generate_single_event_data("MAN_6K"), ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(426, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_wom_5k_event(self):
        athletics_event.interactive_main(generate_single_event_data("WOM_5K"), ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(265, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_10k_event(self):
        man_10k_event_data = generate_single_event_data("MAN_10K")
        athletics_event.interactive_main(man_10k_event_data, ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(397, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(man_10k_event_data, ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(589, athletics_event.event.scenario.objective_value())

    def no_test_interactive_main_wom_7K_event(self):
        wom_7k_event_data = generate_single_event_data("WOM_7K")
        athletics_event.interactive_main(wom_7k_event_data, ["saturday", "--ratio-gap=1", "--silent"])
        self.assertEqual(138, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(wom_7k_event_data, ["sunday", "--ratio-gap=1", "--silent"])
        self.assertEqual(97, athletics_event.event.scenario.objective_value())
