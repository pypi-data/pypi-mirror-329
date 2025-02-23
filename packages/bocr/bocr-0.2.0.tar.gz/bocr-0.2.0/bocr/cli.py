import argparse
import inspect
import re
from typing import Dict

from bocr import Config, ocr


def get_config_metadata() -> Dict[str, Dict[str, str]]:
    """
    Extracts metadata from the `Config` class, including attribute names, types, and descriptions.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where each key is an attribute name,
        and the value is a dictionary containing the attribute's type and description.
    """
    docstring = inspect.getdoc(Config) or ""
    attributes_section = re.search(r"Attributes:\s*(.*)", docstring, re.DOTALL)
    attributes = attributes_section.group(1) if attributes_section else ""

    parameter_pattern = r"^\s*(\w+)\s*\(?(.*?)\)?\s*:\s*(.+?)(?=\n\s*\w+\s*\(|\n\s*\w+\s*:|\Z)"
    parameter_matches = re.findall(parameter_pattern, attributes, re.MULTILINE | re.DOTALL)

    return {
        param: {"type": dtype.strip(), "description": re.sub(r'\s+', ' ', desc).strip()}
        for param, dtype, desc in parameter_matches
    }


def parse_args() -> argparse.Namespace:
    """
    Dynamically generates and parses command-line arguments based on `Config` class metadata.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    metadata = get_config_metadata()
    parser = argparse.ArgumentParser(
        description="Perform document OCR using Vision LLMs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    config_instance = Config()
    for key, default in vars(config_instance).items():
        meta = metadata.get(key, {"type": type(default).__name__, "description": ""})
        arg_type = {"int": int, "float": float}.get(meta["type"].lower(), type(default or ""))
        is_boolean = isinstance(default, bool)

        parser.add_argument(
            f"--{key.replace('_', '-')}",
            **({"action": "store_false" if default else "store_true"} if is_boolean else
               {"type": arg_type, "default": default}),
            help=meta['description']
        )

    parser.add_argument("files", nargs="+", help="Input files (images, PDFs, or URLs) to process.")

    return parser.parse_args()


def main() -> None:
    """Run OCR based on parsed CLI arguments."""
    args = parse_args()
    config_args = {k: v for k, v in vars(args).items() if k != "files"}
    result = ocr(args.files, Config(**config_args))
    print(result)


if __name__ == "__main__":
    main()
