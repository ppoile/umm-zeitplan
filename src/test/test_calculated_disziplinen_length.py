import copy
import unittest

import athletics_event
from .u12w_4k_event_data import event_data as u12w_4k_event_data


class TestCalculatedDisziplinenLength(unittest.TestCase):
    def setUp(self):
        self.event_data = copy.deepcopy(u12w_4k_event_data)

    def test_u12w_60m(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr14_60m"].length)
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr15_to_Gr16_60m"].length)
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr17_60m"].length)
        self.assertEqual(2, athletics_event.event._disziplinen["U12W_4K_Gr18_60m"].length)

    def test_u12w_kugel(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr14_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr15_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr16_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr17_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr18_Kugel"].length)

    def test_u12w_weit(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr14_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr15_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr16_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr17_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr18_Weit"].length)

    def test_u12w_600m(self):
        athletics_event.interactive_main(self.event_data, ["saturday", "--print-scenario-and-exit"])
        self.assertEqual(6, athletics_event.event._disziplinen["U12W_4K_Gr14_to_Gr18_600m"].length)

    def test_u12w_60m_get_calculated_disziplinen_length(self):
        event = athletics_event.AthleticsEventScheduler("test_event", athletics_event.default_arguments["horizon"])
        self.assertEqual(0, event._get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=0, num_anlagen=1, exact=False))
        self.assertEqual(1, event._get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=1, num_anlagen=1, exact=False))
        self.assertEqual(0.2, event._get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=1, num_anlagen=1, exact=True))
        self.assertEqual(1, event._get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=5 * 6, num_anlagen=1, exact=False))
        self.assertEqual(2, event._get_calculated_disziplinen_length(wettkampf=None, disziplin="60m", num_athletes=5 * 6 + 1, num_anlagen=1, exact=False))

    def test_u12w_60m_create_disziplinen(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr14": 12,
            "Gr15": 12,
            "Gr16": 12,
            "Gr17": 12,
            "Gr18": 12,
            "Gr19": 12,
        }
        event = athletics_event.AthleticsEventScheduler("test_event", athletics_event.default_arguments["horizon"])
        event.create_anlagen(self.event_data['anlagen_descriptors']["saturday"])
        event.create_disziplinen(self.event_data['wettkampf_data']["saturday"], self.event_data['teilnehmer_data'])
        self.assertEqual(1, event._disziplinen["U12W_4K_Gr14_to_Gr15_60m"].length)
        self.assertEqual(1, event._disziplinen["U12W_4K_Gr16_to_Gr18_60m"].length)
        self.assertEqual(2, event._disziplinen["U12W_4K_Gr19_60m"].length)

    def test_u12w_60m_create_disziplinen_2(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr14": 5*6,
            "Gr15": 1*6,
        }
        event = athletics_event.AthleticsEventScheduler("test_event", athletics_event.default_arguments["horizon"])
        event.create_anlagen(self.event_data['anlagen_descriptors']["saturday"])
        event.create_disziplinen(self.event_data['wettkampf_data']["saturday"], self.event_data['teilnehmer_data'])
        self.assertEqual(1, event._disziplinen["U12W_4K_Gr14_60m"].length)
        self.assertEqual(2, event._disziplinen["U12W_4K_Gr15_60m"].length)

    def no_test_u12w_60m_create_disziplinen_3(self):
        self.event_data['teilnehmer_data']["U12W_4K"] = {
            "Gr14": 10*6,
            "Gr15": 1*6,
        }
        event = athletics_event.AthleticsEventScheduler("test_event", athletics_event.default_arguments["horizon"])
        event.create_anlagen(self.event_data['anlagen_descriptors']["saturday"])
        event.create_disziplinen(self.event_data['wettkampf_data']["saturday"], self.event_data['teilnehmer_data'])
        self.assertEqual(2, event._disziplinen["U12W_4K_Gr14_60m"].length)
        self.assertEqual(2, event._disziplinen["U12W_4K_Gr15_60m"].length)
