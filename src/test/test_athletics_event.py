import unittest

import athletics_event


class TestAthleticsEvent(unittest.TestCase):
    def test_instantiate_AthleticsEventScheduler(self):
        athletics_event.AthleticsEventScheduler(name="TestEvent", duration_in_units=athletics_event.default_arguments["horizon"])

    def test_interactive_main_u12w_4k_event(self):
        from u12w_4k_event import event_data as u12w_4k_event_data
        athletics_event.interactive_main(u12w_4k_event_data, ["saturday"])
        self.assertEqual(300, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_6k_event(self):
        from man_6k_event import event_data as man_6k_event_data
        athletics_event.interactive_main(man_6k_event_data, ["sunday"])
        self.assertEqual(419, athletics_event.event.scenario.objective_value())

    def test_interactive_main_man_10k_event(self):
        from man_10k_event import event_data as man_10k_event_data
        athletics_event.interactive_main(man_10k_event_data, ["saturday"])
        self.assertEqual(397, athletics_event.event.scenario.objective_value())
        athletics_event.interactive_main(man_10k_event_data, ["sunday"])
        self.assertEqual(589, athletics_event.event.scenario.objective_value())
