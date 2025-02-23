import logging
from typing import Dict, List, Union

from bocr import Config
from bocr.utils.logger import configure_logging
from bocr.backbones.backbone import get_extract_text
from bocr.preprocessing.preprocess import prepare_inputs
from bocr.postprocessing.postprocess import postprocess

logger = logging.getLogger(__name__)


def ocr(
    input_paths: Union[str, List[str]], config: Config
) -> Union[str, List[str], Dict[str, Union[str, List[str]]], None]:
    """
    Perform OCR on input files using Vision LLMs with the provided configuration.

    Args:
        input_paths (Union[str, List[str]]): Path(s) to input images or documents.
        config (Config): Configuration object for OCR settings.

    Returns:
        Union[str, List[str], Dict[str, Union[str, List[str]]], None]: OCR results. For a single input, returns a
            string; for a list of one-page inputs, returns a list of strings; for multiple inputs or if saving outputs,
            returns a dictionary mapping input paths to results and output paths. Returns None in case of errors.
    """
    configure_logging(config.verbose)

    # noinspection PyBroadException
    try:
        input_paths = [input_paths] if isinstance(input_paths, str) else input_paths
        logger.info(f"Starting OCR with config: {config}")

        extract_text = get_extract_text(config)

        # Preprocess inputs and perform OCR
        with prepare_inputs(input_paths, config) as prepared_files:
            total_files = len(prepared_files)
            raw_results = {}

            for file_number, (file_path, image_list) in enumerate(prepared_files.items(), start=1):
                extracted_texts = []
                total_images = len(image_list)

                for image_number, image_path in enumerate(image_list, start=1):
                    logger.info(
                        f"Processing file {file_number}/{total_files} ({file_path}) | "
                        f"Image {image_number}/{total_images}: {image_path}"
                    )
                    # Perform OCR
                    text = extract_text(image_path, config.prompt, config.model_id, config.max_new_tokens)
                    extracted_texts.append(text)

                raw_results[file_path] = extracted_texts

        # Postprocess results
        logger.info("Postprocessing OCR results.")
        processed_results = postprocess(raw_results, config)

        # Return results
        logger.info("OCR completed successfully.")
        return processed_results[input_paths[0]] if len(input_paths) == 1 else processed_results

    except Exception:
        logger.exception("OCR process failed.")
        return None
