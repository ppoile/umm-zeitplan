"""Assemble event data for your event and call interactive_main()"""

event_data = {
    'event_name': 'Uster Mehrkampf Meeting',
    'anlagen_descriptors': {
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
        "sunday": {
            "MAN_6K": {
                "disziplinen": [
                    dict(name="100m", together=True, keep_groups_separate=True, resource="Läufe", length=2),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=3),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=3),
                    dict(name="Hoch", resource="Hoch", length=3),
                    dict(name="Pause_4", length=3),
                    dict(name="Speer", resource="Speer&Diskus", length=3),
                    dict(name="Pause_5", length=3),
                    dict(name="1000m", together=True, resource="Läufe", length=2),
                ],
                "plot_color": "lightblue",
            },
        }
    },
    'wettkampf_start_times': {
        "sunday": {
            #"WOM_7K_.*_Weit": 9,
            #"MAN_10K_.*_110mHü": 18,
        },
    },
    'wettkampf_start_sequence': {
        "saturday": [
            "U16M_6K_.*_100mHü",
            "U16W_5K_.*_80m",
            "U12M_4K_.*_60m",
            "U12W_4K_.*_60m",
            #"WOM_7K_.*_100mHü",
            #"MAN_10K_.*_100m",
        ],
        "sunday": [
            "MAN_6K_.*_100m",
            "U14W_5K_.*_60m",
            "WOM_5K_.*_100m",
            "U14M_5K_.*_60m",
            #"WOM_7K_.*_100mHü",
            #"MAN_10K_.*_100m",
        ],
    },
    'teilnehmer_data': {
        "MAN_6K": {
            "Gr38": 18,
            "Gr39": 10,
            "Gr40": 18,
        },
    },
    'maximum_wettkampf_duration': {
        "sunday": {
            "U14W_5K": 31,
            "WOM_7K": 18,
            "WOM_5K": 28,
            "U14M_5K": 26,
            "MAN_10K": 39,
            "MAN_6K": 41,
        },
    },
}


if __name__ == "__main__":
    import athletics_event
    athletics_event.interactive_main(event_data)
