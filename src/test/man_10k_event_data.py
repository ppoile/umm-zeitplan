"""Assemble event data for your event and call interactive_main()"""

event_data = {
    'event_name': 'MAN 10-K Test Event',
    'event_name_short': 'man_10k',
    'anlagen_descriptors': {
        'saturday': [
            ("Läufe",),
            ("Weit", 3),
            ("Kugel", 2),
            ("Hoch", 2),
            ("Diskus",),
        ],
        'sunday': [
            ("Läufe",),
            ("Weit", 3),
            ("Kugel", 2),
            ("Hoch", 2),
            ("Diskus",),
            ("Speer",),
            ("Stab",),
        ],
    },
    'wettkampf_data': {
        'saturday': {
            "MAN_10K": {
                "disziplinen": [
                    dict(name="100m", together=True, resource="Läufe", length=2),
                    dict(name="Pause_1", length=4),
                    dict(name="Weit", together=True, resource="Weit1&Weit2&Weit3", use_num_anlagen=2, length=3),  # auf Weit1 und Weit2
                    dict(name="Pause_2", length=3),
                    dict(name="Kugel", resource="Kugel", length=4),
                    dict(name="Pause_3", length=3),
                    dict(name="Hoch", together=True, resource="Hoch1&Hoch2", use_num_anlagen=2, length=7),  # auf Hoch1 und Hoch2
                    dict(name="Pause_4", length=4),
                    dict(name="400m", together=True, resource="Läufe", length=3),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "is_last_wettkampf_of_the_day": True,
                "plot_color": "red",
            },
        },
        "sunday": {
            "MAN_10K": {
                "disziplinen": [
                    dict(name="110mHü", together=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Diskus", together=True, resource="Diskus&Speer", length=4),
                    dict(name="Pause_2", length=4),
                    dict(name="Stab", together=True, resource="Stab", length=9),
                    dict(name="Pause_3", length=3),
                    dict(name="Speer", together=True, resource="Speer&Diskus", length=4),
                    dict(name="Pause_4", length=3),
                    dict(name="1500m", together=True, resource="Läufe", length=3),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "is_last_wettkampf_of_the_day": True,
                "plot_color": "red",

            },
        }
    },
    'wettkampf_start_times': {
        "saturday": {
            "MAN_10K_.*_100m": 9,
        },
        "sunday": {
            "MAN_10K_.*_110mHü": 18,
        },
    },
    'teilnehmer_data': {
        "MAN_10K": {
            "Gr23": 10,
            "Gr24": 10,
        },
    },
    'maximum_wettkampf_duration': {
        "saturday": {
            "MAN_10K": 33,
        },
        "sunday": {
            "MAN_10K": 39,
        },
    },
}
