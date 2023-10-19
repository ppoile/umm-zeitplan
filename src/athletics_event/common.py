# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,line-too-long

import logging


class SomethingWentWrong(RuntimeError):
    pass


class NoSolutionError(RuntimeError):
    pass


def setup_logging(verbose, event_name):
    # dont do anything if logging has already been configured
    if len(logging.root.handlers) > 0:
        return

    log_level = logging.INFO
    if verbose:
        log_level=logging.DEBUG
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f'{event_name}.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    root_logger.addHandler(ch)
    root_logger.addHandler(fh)
    matplotlib_logger = logging.getLogger("matplotlib")
    matplotlib_logger.setLevel(logging.INFO)
    zeitplan_logger = logging.getLogger("zeitplan")
    zeitplan_logger.setLevel(logging.INFO)
