"""Assemble event data for your event and call interactive_main()"""

event_data = {
    'event_name': 'U12W 4-K Test Event',
    'event_name_short': 'u12w_4k',
    'anlagen_descriptors': {
        'saturday': [
            ("Läufe",),
            ("Weit", 3),
            ("Kugel", 2),
            ("Hoch", 2),
            ("Diskus",),
        ],
    },
    'wettkampf_data': {
        'saturday': {
            "U12W_4K": {
                "disziplinen": [
                    dict(name="60m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=2),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=1),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "orange",
            },
        },
    },
    'wettkampf_start_times': {
        "saturday": {
        },
    },
    'teilnehmer_data': {
        "U12W_4K": {
            "Gr14": 15,
            "Gr15": 14,
            "Gr16": 14,
            "Gr17": 14,
            "Gr18": 14,
        },
    },
    'maximum_wettkampf_duration': {
        "saturday": {
            "U12W_4K": 27,
        },
    },
}
