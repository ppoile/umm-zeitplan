import logging
import sys


def setup_logging():
    if "-vv" in sys.argv[1:]:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("zeitplan").setLevel(logging.WARNING)
        logging.getLogger("matplotlib").setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=logging.WARNING)
