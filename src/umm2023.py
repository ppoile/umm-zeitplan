"""Assemble event data for your event and call interactive_main()"""

event_data = {
    'event_name': 'Uster Mehrkampf Meeting 2023',
    'event_name_short': 'umm2023',
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
            "U12W_4K": {
                "disziplinen": [
                    dict(name="60m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=1),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "orange",
            },
            "U16W_5K": {
                "disziplinen": [
                    dict(name="80m", together=True, keep_groups_separate=True, resource="Läufe", length=2),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=2),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=2),
                    dict(name="Hoch", resource="Hoch", length=5),
                    dict(name="Pause_4", length=3),
                    dict(name="1000m", together=True, resource="Läufe", length=2),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "plot_color": "pink",
            },
            "WOM_7K": {
                "disziplinen": [
                    dict(name="100mHü", together=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=4),
                    dict(name="Hoch", together=True, resource="Hoch1&Hoch2", use_num_anlagen=2, length=5),
                    dict(name="Pause_2", length=3),
                    dict(name="Kugel", resource="Kugel", length=3),
                    dict(name="Pause_3", length=4),
                    dict(name="200m", together=True, resource="Läufe", length=2),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "plot_color": "lightgreen",
            },
            "U12M_4K": {
                "disziplinen": [
                    dict(name="60m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=1),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "yellow",
            },
            "U16M_6K": {
                "disziplinen": [
                    dict(name="100mHü", together=True, keep_groups_separate=True, resource="Läufe", length=2),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=2),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=2),
                    dict(name="Hoch", resource="Hoch", length=5),
                    dict(name="Pause_4", length=2),
                    dict(name="Diskus", resource="Diskus", length=5),
                    dict(name="Pause_5", length=3),
                    dict(name="1000m", together=True, resource="Läufe", length=2),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "plot_color": "lightblue",
            },
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
            "U14M_5K": {
                "disziplinen": [
                    dict(name="60m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=1),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=1),
                    dict(name="Hoch", resource="Hoch", length=3),
                    dict(name="Pause_4", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "orange",
            },
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
            "WOM_5K": {
                "disziplinen": [
                    dict(name="100m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=4),
                    dict(name="Pause_2", length=3),
                    dict(name="Kugel", resource="Kugel", length=3),
                    dict(name="Pause_3", length=3),
                    dict(name="Hoch", resource="Hoch", length=4),
                    dict(name="Pause_4", length=3),
                    dict(name="1000m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "olive",
            },
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
            "U14W_5K": {
                "disziplinen": [
                    dict(name="60m", together=True, keep_groups_separate=True, resource="Läufe", length=3),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=1),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=1),
                    dict(name="Hoch", resource="Hoch", length=3),
                    dict(name="Pause_4", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=3),
                ],
                "plot_color": "pink",
            },
            "WOM_7K": {
                "disziplinen": [
                    dict(name="Weit", together=True, resource="Weit1&Weit2&Weit3", use_num_anlagen=2, length=4),  # auf Weit1 und Weit2
                    dict(name="Pause_1", length=3),
                    dict(name="Speer", resource="Speer&Diskus", length=4),
                    dict(name="Pause_2", length=3),
                    dict(name="800m", together=True, resource="Läufe", length=4),
                ],
                "is_wettkampf_with_strict_sequence": True,
                "plot_color": "lightgreen",
            },
        }
    },
    'wettkampf_start_times': {
        "saturday": {
            "WOM_7K_.*_100mHü": 9,
            "MAN_10K_.*_100m": 9,
        },
        "sunday": {
            "WOM_7K_.*_Weit": 9,
            "MAN_10K_.*_110mHü": 18,
        },
    },
    'teilnehmer_data': {
        "WOM_7K": {
            "Gr1": 12,
            "Gr2": 13,
        },
        "U16W_5K": {
            "Gr3": 16,
            "Gr4": 16,
            "Gr5": 16,
        },
        "U14W_5K": {
            "Gr6": 14,
            "Gr7": 13,
            "Gr8": 13,
            "Gr9": 14,
            "Gr10": 13,
            "Gr11": 13,
            "Gr12": 13,
            "Gr13": 13,
        },
        "U12W_4K": {
            "Gr14": 15,
            "Gr15": 14,
            "Gr16": 14,
            "Gr17": 14,
            "Gr18": 14,
        },
        "WOM_5K": {
            "Gr20": 9,
            "Gr21": 10,
            "Gr22": 15,
        },
        "MAN_10K": {
            "Gr23": 10,
            "Gr24": 10,
        },
        "U16M_6K": {
            "Gr25": 13,
            "Gr26": 13,
            "Gr27": 13,
        },
        "U14M_5K": {
            "Gr28": 14,
            "Gr29": 14,
            "Gr30": 14,
            "Gr31": 14,
        },
        "U12M_4K": {
            "Gr33": 13,
            "Gr34": 13,
            "Gr35": 13,
            "Gr36": 12,
        },
        "MAN_6K": {
            "Gr38": 18,
            "Gr39": 10,
            "Gr40": 18,
        },
    },
}


if __name__ == "__main__":
    import athletics_event
    athletics_event.interactive_main(event_data)
