import logging
import os
import tempfile
from contextlib import contextmanager
from typing import List, Dict, Union
from urllib.parse import urlparse

import cv2
import requests
from pdf2image import convert_from_path

from bocr import Config

logger = logging.getLogger(__name__)


def preprocess_image(image_path: str, output_dir: str, max_size: Union[int, None] = None) -> str:
    """
    Preprocess an image for OCR by resizing and enhancing its quality.

    Args:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the preprocessed image.
        max_size (Union[int, None], optional): Maximum allowed size for the largest image dimension. Defaults to None.

    Returns:
        str: Path to the preprocessed image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image {image_path}.")

    # Denoising
    denoised = cv2.fastNlMeansDenoisingColored(image, None, h=5, hColor=5, templateWindowSize=7, searchWindowSize=21)

    # Contrast enhancement
    lab_image = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
    enhanced_l_channel = clahe.apply(l_channel)
    enhanced_image = cv2.merge((enhanced_l_channel, a_channel, b_channel))
    contrast_enhanced = cv2.cvtColor(enhanced_image, cv2.COLOR_LAB2BGR)

    # Resize if needed
    if max_size:
        height, width, _ = contrast_enhanced.shape
        largest_side = max(width, height)
        if largest_side > max_size:
            scale = max_size / largest_side
            new_width = int(width * scale)
            new_height = int(height * scale)
            logger.debug(f"Resizing image from {width}x{height} to {new_width}x{new_height}.")
            contrast_enhanced = cv2.resize(contrast_enhanced, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Save preprocessed image
    preprocessed_path = os.path.join(output_dir, f"preprocessed_{os.path.basename(image_path)}")
    cv2.imwrite(preprocessed_path, contrast_enhanced)
    logger.debug(f"Preprocessed image saved to `{preprocessed_path}`.")
    return preprocessed_path


def is_valid_url(url: str) -> bool:
    """
    Check if a given string is a valid URL.

    Args:
        url (str): URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


def download_file(url: str, output_dir: str) -> str:
    """
    Download a file from a URL to the specified directory.

    Args:
        url (str): URL of the file to download.
        output_dir (str): Directory to save the downloaded file.

    Returns:
        str: Path to the downloaded file.
    """
    logger.debug(f"Downloading `{url}`.")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    downloaded_path = os.path.join(output_dir, os.path.basename(url))
    with open(downloaded_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    logger.debug(f"Downloaded file saved to `{downloaded_path}`.")
    return downloaded_path


@contextmanager
def prepare_inputs(
    input_paths: List[str],
    config: Config,
) -> Dict[Union[int, str], List[str]]:
    """
    Prepare input files for OCR by downloading URLs, converting PDFs to images, preprocessing images if needed, and
    managing temporary files.

    Args:
        input_paths (List[str]): List of input paths (file paths or URLs).
        config (Config): Configuration object containing preprocessing and other settings.

    Yields:
        Dict[Union[int, str], List[str]]: Mapping of input files to their corresponding preprocessed image paths.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        file_mapping = {}

        for input_path in input_paths:
            logger.info(f"Processing `{input_path}`.")

            # Handle URLs or local files
            if is_valid_url(input_path):
                input_path = download_file(input_path, temp_dir)
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file `{input_path}` not found!")

            # Convert PDFs to images
            if input_path.lower().endswith(".pdf"):
                image_paths = convert_from_path(
                    input_path, dpi=config.resolution, output_folder=temp_dir, fmt="png", paths_only=True
                )
                if config.preprocess:
                    image_paths = [
                        preprocess_image(image, temp_dir, config.max_image_size)  # type: ignore
                        for image in image_paths
                    ]
                file_mapping[input_path] = image_paths

            # Handle image files
            elif input_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                if config.preprocess:
                    preprocessed_image = preprocess_image(input_path, temp_dir, max_size=config.max_image_size)
                    file_mapping[input_path] = [preprocessed_image]
                else:
                    file_mapping[input_path] = [input_path]

            else:
                raise ValueError(f"Unsupported file type `{input_path}`. Supported: PDFs, images, and URLs.")

        yield file_mapping
