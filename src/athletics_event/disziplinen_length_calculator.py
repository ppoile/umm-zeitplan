# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long

import logging
import math


def get_calculated_disziplinen_length(wettkampf, disziplin, num_athletes, num_anlagen, exact=False):
    mapping = {
        "60m": (6, 2/10),
        "80m": (6, 2/10),
        "80mHü": (6, 4/10),
        "100m": (6, 2/10),
        "100mHü": (6, 4/10),
        "110mHü": (6, 4/10),
        "200m": (6, 4/10),
        "400m": (6, 7/10),
        "800m": (6, 7/10),
        "600m": (16, 1),
        "1000m": (16, 1),
        "1500m": (16, 1),
        "Diskus": (1, 3/15),
        "Hoch": {
            "U14W_5K": (1, 3/15),
            "U14M_5K": (1, 3/15),
            "U16W_5K": (1, 5/15),
            "U16M_6K": (1, 5/15),
            "WOM_5K": (1, 3/15),
            "WOM_7K": (1, 5/15),
            "MAN_6K": (1, 3/15),
            "MAN_10K": (1, 5/15),
        },
        "Kugel": (1, 2/15),
        "Speer": (1, 3/12),
        "Stab": (1, 6/12),
        "Weit": (1, 3/15),
    }
    item = mapping[disziplin]
    if isinstance(item, dict):
        item = item[wettkampf]
    num_serien = ((num_athletes - 1) // item[0]) + 1
    calculated_length = num_serien * item[1]
    calculated_length = calculated_length / num_anlagen
    if not exact:
        calculated_length = math.ceil(calculated_length)
    logging.debug("      get_calculated_disziplinen_length(wettkampf=%s, disziplin=%s, num_athletes=%s, num_anlagen=%s, exact=%s) => %s", wettkampf, disziplin, num_athletes, num_anlagen, exact, round(calculated_length, 3))
    return calculated_length
