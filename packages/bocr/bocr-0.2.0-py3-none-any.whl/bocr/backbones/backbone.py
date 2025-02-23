import importlib
import logging
import os
import re
from typing import Callable

import yaml

from bocr import Config

logger = logging.getLogger(__name__)

BACKBONE_MAPPING_FILE_PATH = os.path.join(os.path.dirname(__file__), 'mapping.yaml')


def resolve_backbone(model_id: str) -> str:
    """
    Resolve the backbone for the given model ID by matching against patterns defined in the mappings YAML file.

    Args:
        model_id (str): Identifier for the model.

    Returns:
        str: The name of the resolved backbone.

    Raises:
        ValueError: If no matching backbone is found for the given model ID.
    """
    with open(BACKBONE_MAPPING_FILE_PATH, "r") as file:
        patterns = yaml.safe_load(file)

    for backbone, regex_list in patterns.items():
        for pattern in regex_list:
            if re.match(pattern, model_id):
                logger.debug(f"Model `{model_id}` resolved to backbone `{backbone}`.")
                return backbone

    raise ValueError(f"Model `{model_id}` does not match any registered backbone.")


def get_extract_text(config: Config) -> Callable:
    """
    Retrieve the `extract_text` method for the resolved backbone based on the given configuration.

    Args:
        config (Config): Configuration object containing model ID and other settings.

    Returns:
        Callable: The `extract_text` function from the resolved backbone.
    """
    backbone = resolve_backbone(config.model_id)
    module = importlib.import_module(f"bocr.backbones.{backbone}")
    logger.debug(f"Successfully loaded module for backbone `{backbone}`.")
    return getattr(module, "extract_text")
