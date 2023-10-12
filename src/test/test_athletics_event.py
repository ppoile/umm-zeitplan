import unittest

import athletics_event


class TestAthleticsEvent(unittest.TestCase):
    def test_instantiate_AthleticsEventScheduler(self):
        from .u12w_4k_event_data import event_data as u12w_4k_event_data
        athletics_event.AthleticsEventScheduler(event_data=u12w_4k_event_data, horizon=athletics_event.default_arguments["horizon"])

    def test_interactive_main_u12w_4k_event(self):
        from .u12w_4k_event_data import event_data as u12w_4k_event_data
        athletics_event.interactive_main(u12w_4k_event_data, ["saturday", "--ratio-gap=1"])
        self.assertEqual(291, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_6k_event(self):
        from .man_6k_event_data import event_data as man_6k_event_data
        athletics_event.interactive_main(man_6k_event_data, ["sunday", "--ratio-gap=1"])
        self.assertEqual(426, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_10k_event(self):
        from .man_10k_event_data import event_data as man_10k_event_data
        athletics_event.interactive_main(man_10k_event_data, ["saturday", "--ratio-gap=1"])
        self.assertEqual(397, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(man_10k_event_data, ["sunday", "--ratio-gap=1"])
        self.assertEqual(589, athletics_event.event.scenario.objective_value())
