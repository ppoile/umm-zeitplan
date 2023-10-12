# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long
import unittest

import athletics_event
from .u12w_4k_event_data import event_data as u12w_4k_event_data


class TestCreateAnlagen(unittest.TestCase):
    def setUp(self):
        self.event = athletics_event.AthleticsEventScheduler(u12w_4k_event_data, "saturday", athletics_event.default_arguments["horizon"])

    def test_create_anlagen(self):
        self.event.create_anlagen()
        expected_anlagen = ['Läufe', 'Weit1', 'Weit2', 'Weit3', 'Kugel1', 'Kugel2', 'Hoch1', 'Hoch2', 'Diskus']
        self.assertListEqual(expected_anlagen, list(self.event.anlagen.keys()))
