# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import unittest

import athletics_event
from athletics_event.disziplinen_length_calculator import get_calculated_disziplinen_length
from .common import setup_logging
from .event_data import generate_single_event_data


setup_logging()


class TestCalculatedDisziplinenLength(unittest.TestCase):
    def setUp(self):
        self.event_data = generate_single_event_data("U12W_4K")

    def test_u12w_60m(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(1, athletics_event.event.scenario["U12W_4K_Gr14_60m"].length)
        self.assertEqual(1, athletics_event.event.scenario["U12W_4K_Gr15_to_Gr16_60m"].length)
        self.assertEqual(2, athletics_event.event.scenario["U12W_4K_Gr17_to_Gr18_60m"].length)

    def test_u12w_kugel(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(3, athletics_event.event.scenario["U12W_4K_Gr14_Kugel"].length)
        self.assertEqual(3, athletics_event.event.scenario["U12W_4K_Gr15_Kugel"].length)
        self.assertEqual(3, athletics_event.event.scenario["U12W_4K_Gr16_Kugel"].length)
        self.assertEqual(3, athletics_event.event.scenario["U12W_4K_Gr17_Kugel"].length)
        self.assertEqual(3, athletics_event.event.scenario["U12W_4K_Gr18_Kugel"].length)

    def test_u12w_weit(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(4, athletics_event.event.scenario["U12W_4K_Gr14_Weit"].length)
        self.assertEqual(4, athletics_event.event.scenario["U12W_4K_Gr15_Weit"].length)
        self.assertEqual(4, athletics_event.event.scenario["U12W_4K_Gr16_Weit"].length)
        self.assertEqual(4, athletics_event.event.scenario["U12W_4K_Gr17_Weit"].length)
        self.assertEqual(4, athletics_event.event.scenario["U12W_4K_Gr18_Weit"].length)

    def test_u12w_600m(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(6, athletics_event.event.scenario["U12W_4K_Gr14_to_Gr18_600m"].length)

    def test_u12w_60m_get_calculated_disziplinen_length(self):
        self.assertEqual(0, get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=0, num_anlagen=1, exact=False))
        self.assertEqual(1, get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=1, num_anlagen=1, exact=False))
        self.assertEqual(0.2, get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=1, num_anlagen=1, exact=True))
        self.assertEqual(1, get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=5 * 6, num_anlagen=1, exact=False))
        self.assertEqual(2, get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=5 * 6 + 1, num_anlagen=1, exact=False))

    def test_u12w_60m_create_disziplinen_five_groups_fit_one_slot(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 1 * 6,
            "Gr2": 1 * 6,
            "Gr3": 1 * 6,
            "Gr4": 1 * 6,
            "Gr5": 1 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(2, event.scenario["U12W_4K_Gr1_to_Gr5_60m"].length)

    def test_u12w_60m_create_disziplinen_fifth_group_overlaps_into_second_slot(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 1 * 6,
            "Gr2": 1 * 6,
            "Gr3": 1 * 6,
            "Gr4": 1 * 6,
            "Gr5": 2 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(1, event.scenario["U12W_4K_Gr1_to_Gr4_60m"].length)
        self.assertEqual(2, event.scenario["U12W_4K_Gr5_60m"].length)

    def test_u12w_60m_create_disziplinen_two_groups_in_two_slots(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 5 * 6,
            "Gr2": 1 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(1, event.scenario["U12W_4K_Gr1_60m"].length)
        self.assertEqual(2, event.scenario["U12W_4K_Gr2_60m"].length)

    def test_u12w_60m_create_disziplinen_group_spans_two_slots(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 5 * 6 + 1,
            "Gr2": 1 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(3, event.scenario["U12W_4K_Gr1_to_Gr2_60m"].length)

    def test_u12w_60m_create_disziplinen_group_spans_two_slots_filled(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 5 * 6 + 1,
            "Gr2": 1 * 6,
            "Gr3": 5 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(2, event.scenario["U12W_4K_Gr1_to_Gr2_60m"].length)
        self.assertEqual(2, event.scenario["U12W_4K_Gr3_60m"].length)

    def test_u12w_60m_create_disziplinen_group_spans_three_slots_filled(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr1": 10 * 6 + 1,
            "Gr2": 1 * 6,
            "Gr3": 5 * 6,
        }
        event = athletics_event.AthleticsEventScheduler(self.event_data, "saturday", athletics_event.default_arguments["horizon"])
        event.create_anlagen()
        event.create_disziplinen()
        self.assertEqual(3, event.scenario["U12W_4K_Gr1_to_Gr2_60m"].length)
        self.assertEqual(2, event.scenario["U12W_4K_Gr3_60m"].length)
