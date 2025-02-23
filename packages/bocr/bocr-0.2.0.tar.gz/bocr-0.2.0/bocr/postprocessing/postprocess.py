import importlib
import logging
import os
from typing import List, Dict

from bocr import Config

logger = logging.getLogger(__name__)


def postprocess(input_results: Dict[str, List[str]], config: Config) -> Dict[str, Dict[str, List[str]]]:
    """
    Postprocess OCR results by merging and optionally saving them in the specified format.

    Args:
        input_results (Dict[str, List[str]]): Mapping of file paths to their OCR page results.
        config (Config): Configuration object containing postprocessing settings.

    Returns:
        Dict[str, Dict[str, List[str]]]: Postprocessed results including saved file paths.
    """
    output_module = importlib.import_module(f"bocr.postprocessing.{config.result_format}")

    # Create output directory if saving outputs
    export_dir = config.export_dir or os.path.join(os.getcwd(), "ocr_exports")
    if config.export_results:
        os.makedirs(export_dir, exist_ok=True)

    processed_results = {}

    # Process each file's OCR results
    for original_path, page_texts in input_results.items():
        logger.info(f"Processing results for: {original_path}")

        # Merge texts if required
        if config.merge_text:
            merge = getattr(output_module, "merge")
            page_texts = [merge(page_texts)]

        # Store extracted result
        processed_results[original_path] = {"extracted_text": page_texts}

        # Save outputs if configured
        if config.export_results:
            saved_files = []
            base_name = os.path.splitext(os.path.basename(original_path))[0]
            export = getattr(output_module, f"export_{config.export_format}")

            for page_number, page_text in enumerate(page_texts, start=1):
                output_name = f"{base_name}{'' if len(page_texts) == 1 else f'-{page_number}'}"
                output_path = os.path.join(export_dir, f"{output_name}.{config.export_format}")
                export(page_text, output_path)
                saved_files.append(output_path)
                logger.info(f"Extracted page {page_number} saved to {output_path}.")

            # Store saved file names
            processed_results[original_path]["saved_files"] = saved_files

    return processed_results
