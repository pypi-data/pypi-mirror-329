from typing import Optional


class Config:
    """
    Configuration for OCR processing.

    Attributes:
        prompt (Optional[str]): Custom prompt string or None to use the model's default prompt.
        model_id (str): Identifier of the Vision LLM model to use.
        max_new_tokens (int): Maximum number of new tokens generated during the response.
        preprocess (bool): Whether to preprocess images before OCR.
        resolution (int): Resolution (DPI) for processing PDFs.
        max_image_size (Optional[int]): Maximum size of the largest image side in pixels. None means no resizing.
        result_format (str): Desired result format for processing (e.g., 'md').
        merge_text (bool): Merge extracted text into a single string.
        export_results (bool): Whether to export the results to files.
        export_format (str): Desired export format for saving results (e.g., 'txt', 'md', 'docx', 'pdf').
        export_dir (Optional[str]): Directory to save output files. If None, defaults to the `ocr_outputs` directory.
        verbose (bool): Whether to enable detailed logging.
    """
    def __init__(
        self,
        prompt: Optional[str] = None,
        model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct",
        max_new_tokens: int = 1024,
        preprocess: bool = False,
        resolution: int = 150,
        max_image_size: Optional[int] = 1920,
        result_format: str = "md",
        merge_text: bool = False,
        export_results: bool = False,
        export_format: str = "md",
        export_dir: Optional[str] = None,
        verbose: bool = False,
    ):
        self.prompt = prompt
        self.model_id = model_id
        self.max_new_tokens = max_new_tokens
        self.preprocess = preprocess
        self.resolution = resolution
        self.max_image_size = max_image_size
        self.result_format = result_format
        self.merge_text = merge_text
        self.export_results = export_results
        self.export_format = export_format
        self.export_dir = export_dir
        self.verbose = verbose
