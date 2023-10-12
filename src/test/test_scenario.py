# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long
import unittest

from copy import deepcopy

import athletics_event
from .man_10k_event_data import event_data as man_10k_event_data_orig
from .man_6k_event_data import event_data as man_6k_event_data_orig


class TestScenario(unittest.TestCase):
    def test_man_6k_event(self):
        man_6k_event_data = deepcopy(man_6k_event_data_orig)
        man_6k_event_data["teilnehmer_data"]["MAN_6K"] = { "Gr1": 12 }
        athletics_event.interactive_main(man_6k_event_data, ["sunday", "--print-scenario-and-exit"])
        expected_precedences = """LAX PRECEDENCES:
MAN_6K_Gr1_Pause_1 < MAN_6K_Gr1_Weit
MAN_6K_Gr1_Pause_1 < MAN_6K_Gr1_Kugel
MAN_6K_Gr1_Pause_1 < MAN_6K_Gr1_Hoch
MAN_6K_Gr1_Pause_1 < MAN_6K_Gr1_Speer
MAN_6K_Gr1_Pause_1 < MAN_6K_Gr1_to_Gr1_1000m
MAN_6K_Gr1_Pause_2 < MAN_6K_Gr1_to_Gr1_1000m
MAN_6K_Gr1_Pause_3 < MAN_6K_Gr1_to_Gr1_1000m
MAN_6K_Gr1_Pause_4 < MAN_6K_Gr1_to_Gr1_1000m
MAN_6K_Gr1_Pause_5 < MAN_6K_Gr1_to_Gr1_1000m

TIGHT PRECEDENCES:
MAN_6K_Gr1_100m <= MAN_6K_Gr1_Pause_1
MAN_6K_Gr1_Weit <= MAN_6K_Gr1_Pause_2
MAN_6K_Gr1_Kugel <= MAN_6K_Gr1_Pause_3
MAN_6K_Gr1_Hoch <= MAN_6K_Gr1_Pause_4
MAN_6K_Gr1_Speer <= MAN_6K_Gr1_Pause_5

###############################################"""
        self.assertIn(expected_precedences, str(athletics_event.event.scenario))

    def test_man_10k_event_one_group(self):
        man_10k_event_data = deepcopy(man_10k_event_data_orig)
        man_10k_event_data["teilnehmer_data"]["MAN_10K"] = { "Gr1": 12 }
        athletics_event.interactive_main(man_10k_event_data, ["saturday", "--print-scenario-and-exit"])
        expected_precedences = """LAX PRECEDENCES:
MAN_10K_Gr1_to_Gr1_100m < MAN_10K_Gr1_Pause_1
MAN_10K_Gr1_Pause_1 < MAN_10K_Gr1_to_Gr1_Weit
MAN_10K_Gr1_to_Gr1_Weit < MAN_10K_Gr1_Pause_2
MAN_10K_Gr1_Pause_2 < MAN_10K_Gr1_Kugel
MAN_10K_Gr1_Kugel < MAN_10K_Gr1_Pause_3
MAN_10K_Gr1_Pause_3 < MAN_10K_Gr1_to_Gr1_Hoch
MAN_10K_Gr1_to_Gr1_Hoch < MAN_10K_Gr1_Pause_4
MAN_10K_Gr1_Pause_4 < MAN_10K_Gr1_to_Gr1_400m

"""
        self.assertIn(expected_precedences, str(athletics_event.event.scenario))
        athletics_event.interactive_main(man_10k_event_data, ["sunday", "--print-scenario-and-exit"])
        expected_precedences = """LAX PRECEDENCES:
MAN_10K_Gr1_to_Gr1_110mHü < MAN_10K_Gr1_Pause_1
MAN_10K_Gr1_Pause_1 < MAN_10K_Gr1_to_Gr1_Diskus
MAN_10K_Gr1_to_Gr1_Diskus < MAN_10K_Gr1_Pause_2
MAN_10K_Gr1_Pause_2 < MAN_10K_Gr1_to_Gr1_Stab
MAN_10K_Gr1_to_Gr1_Stab < MAN_10K_Gr1_Pause_3
MAN_10K_Gr1_Pause_3 < MAN_10K_Gr1_to_Gr1_Speer
MAN_10K_Gr1_to_Gr1_Speer < MAN_10K_Gr1_Pause_4
MAN_10K_Gr1_Pause_4 < MAN_10K_Gr1_to_Gr1_1500m

"""
        self.assertIn(expected_precedences, str(athletics_event.event.scenario))
