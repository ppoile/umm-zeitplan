"""Assemble event data for your event and call interactive_main()"""

event_data = {
    'event_name': 'Uster Mehrkampf Meeting 2024',
    'event_name_short': 'umm2024',
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
                    dict(name="80mHü", together=True, keep_groups_separate=True, resource="Läufe", length=2),
                    dict(name="Pause_1", length=3),
                    dict(name="Weit", resource="Weit", length=3),
                    dict(name="Pause_2", length=2),
                    dict(name="Kugel", resource="Kugel", length=2),
                    dict(name="Pause_3", length=2),
                    dict(name="Hoch", resource="Hoch", length=5),
                    dict(name="Pause_4", length=3),
                    dict(name="600m", together=True, resource="Läufe", length=2),
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
                    dict(name="Diskus", resource="Diskus&Speer", length=4),
                    dict(name="Pause_2", length=4),
                    dict(name="Stab", together=True, resource="Stab", length=9),
                    dict(name="Pause_3", length=3),
                    dict(name="Speer", resource="Speer&Diskus", length=4),
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
            "MAN_10K_.*_110mHü": 9,
        },
    },
    'teilnehmer_data': {
        "WOM_7K": {
            "Gr1": 13,
            "Gr2": 16,
        },
        "U16W_5K": {
            "Gr3": 13,
            "Gr4": 13,
            "Gr5": 13,
            "Gr6": 13,
            "Gr7": 13,
            "Gr8": 13,
        },
        "U14W_5K": {
            "Gr9": 14,
            "Gr10": 14,
            "Gr11": 14,
            "Gr12": 14,
            "Gr13": 14,
            "Gr14": 14,
            "Gr15": 14,
            "Gr16": 14,
        },
        "U12W_4K": {
            "Gr17": 13,
            "Gr18": 13,
            "Gr19": 13,
            "Gr20": 13,
            "Gr21": 13,
            "Gr22": 13,
        },
        "WOM_5K": {
            "Gr23": 16,
            "Gr24": 7,
            "Gr25": 16,
        },
        "MAN_10K": {
            "Gr26": 18,
            "Gr28": 15,
        },
        "U16M_6K": {
            "Gr29": 14,
            "Gr30": 14,
            "Gr31": 14,
        },
        "U14M_5K": {
            "Gr32": 13,
            "Gr33": 13,
            "Gr34": 13,
            "Gr35": 13,
            "Gr36": 13,
        },
        "U12M_4K": {
            "Gr37": 13,
            "Gr38": 13,
            "Gr39": 13,
            "Gr40": 13,
        },
        "MAN_6K": {
            "Gr41": 14,
            "Gr42": 14,
            "Gr43": 11,
            "Gr44": 15,
        },
    },
}


if __name__ == "__main__":
    import athletics_event
    athletics_event.interactive_main(event_data)
