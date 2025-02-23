import logging
from typing import Optional

import ollama

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = ("""
You are an advanced OCR system. Transcribe the text from the image exactly as it appears, using valid Markdown
syntax (#, ##, ###, -, *, 1., `, ```, >, ---, [ ]( ), ![ ]( ), **, ***, _, __, ~~, |, :---, ---:, :---:) to
accurately capture the style and layout. Do not add explanations, metadata, or notes beyond the exact text
itself, and ensure no part of the text is omitted. Replace unreadable or partially obscured text with [...].
""").replace("\n", " ").strip()


def extract_text(
    image_path: str,
    prompt: Optional[str] = None,
    model_id: str = "llama3.2-vision:11b",
    max_new_tokens: int = 1024,
) -> str:
    """
    Extract text from an image using Ollama backbone.

    Args:
        image_path (str): Path to the input image.
        prompt (Optional[str]): User-provided prompt. If None, the default prompt is used.
        model_id (str): Name or path of the model in Ollama package.
        max_new_tokens (int): Maximum number of tokens to be generated.

    Returns:
        str: The extracted text from the image.
    """
    logger.debug(f"Starting OCR with Ollama package backbone `{model_id}`.")

    # Prepare input messages
    prompt = prompt or DEFAULT_PROMPT
    messages = [{"role": "user", "content": prompt, "images": [image_path]}]

    # Generate response
    response = ollama.chat(
        model=model_id,
        messages=messages,
        options={"num_predict": max_new_tokens, "temperature": 0, "top_p": 1, "top_k": 0},
    )
    extracted_text = response.message.content
    logger.debug(f"Extracted text: {extracted_text}")

    return extracted_text
