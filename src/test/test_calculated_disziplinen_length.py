import unittest

import athletics_event
from .u12w_4k_event_data import event_data as u12w_4k_event_data


class TestCalculatedDisziplinenLength(unittest.TestCase):
    def setUp(self):
        athletics_event.interactive_main(u12w_4k_event_data, ["saturday", "--print-scenario-and-exit"])

    def test_u12w_60m(self):
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr14_60m"].length)
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr15_to_Gr16_60m"].length)
        self.assertEqual(1, athletics_event.event._disziplinen["U12W_4K_Gr17_60m"].length)
        self.assertEqual(2, athletics_event.event._disziplinen["U12W_4K_Gr18_60m"].length)

    def test_u12w_kugel(self):
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr14_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr15_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr16_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr17_Kugel"].length)
        self.assertEqual(3, athletics_event.event._disziplinen["U12W_4K_Gr18_Kugel"].length)

    def test_u12w_weit(self):
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr14_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr15_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr16_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr17_Weit"].length)
        self.assertEqual(4, athletics_event.event._disziplinen["U12W_4K_Gr18_Weit"].length)

    def test_u12w_600m(self):
        self.assertEqual(6, athletics_event.event._disziplinen["U12W_4K_Gr14_to_Gr18_600m"].length)
