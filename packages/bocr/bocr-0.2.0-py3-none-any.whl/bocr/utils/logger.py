import logging
import sys

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging(verbose: bool = False) -> None:
    """
    Configures centralized logging for the entire package.

    Args:
        verbose (bool): If True, sets logging level to DEBUG. Otherwise, INFO.
    """
    root_package = __name__.split(".")[0]
    logging_level = logging.DEBUG if verbose else logging.INFO

    logger = logging.getLogger(root_package)
    logger.setLevel(logging_level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
