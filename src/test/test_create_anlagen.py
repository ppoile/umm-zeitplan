import unittest

import athletics_event
from .u12w_4k_event_data import event_data as u12w_4k_event_data


class TestCreateAnlagen(unittest.TestCase):
    def setUp(self):
        self.argument_day = "saturday"
        self.event = athletics_event.AthleticsEventScheduler(u12w_4k_event_data, athletics_event.default_arguments["horizon"])

    def test_create_anlagen(self):
        self.event.create_anlagen(u12w_4k_event_data['anlagen_descriptors'][self.argument_day])
        expected_anlagen = ['Läufe', 'Weit1', 'Weit2', 'Weit3', 'Kugel1', 'Kugel2', 'Hoch1', 'Hoch2', 'Diskus']
        self.assertListEqual(expected_anlagen, list(self.event.anlagen.keys()))
