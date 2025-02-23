import logging
import re
from typing import Optional

from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = """
You are an advanced OCR system. Transcribe the text from the image exactly as it appears, using valid Markdown
syntax (#, ##, ###, -, *, 1., `, ```, >, ---, [ ]( ),![ ]( ), **, ***, _, __, ~~, |, :---, ---:, :---:) to
accurately capture the style and layout. Do not add explanations, metadata, or notes beyond the exact text
itself, and ensure no part of the text is omitted. Replace unreadable or partially obscured text with [...].
Do not include any extra words, phrases, or explanations beyond what is in the image.
""".replace("\n", " ").strip()


def extract_text(
    image_path: str,
    prompt: Optional[str] = None,
    model_id: str = "meta-llama/Llama-3.2-11B-Vision-Instruct",
    max_new_tokens: int = 1024,
) -> str:
    """
    Extract text from an image using the Llama backbone.

    Args:
        image_path (str): Path to the input image.
        prompt (Optional[str]): User-provided prompt. If None, the default prompt is used.
        model_id (str): Name or path of the Llama model.
        max_new_tokens (int): Maximum number of tokens to be generated.

    Returns:
        str: The extracted text from the image.
    """
    logger.debug(f"Starting OCR with Llama backbone `{model_id}`.")

    # Load the model and processor
    model = MllamaForConditionalGeneration.from_pretrained(model_id, torch_dtype="auto", device_map="auto")
    processor = AutoProcessor.from_pretrained(model_id)

    # Prepare input messages
    prompt = prompt or DEFAULT_PROMPT
    messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]

    # Prepare inputs for the model
    formatted_prompt = processor.apply_chat_template(messages, tokenize=False)
    logger.debug(f"Formatted prompt: {formatted_prompt}")
    image = Image.open(image_path)
    inputs = processor(image, formatted_prompt, add_special_tokens=False, return_tensors="pt").to(model.device)

    # Generate response
    output = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=None,
        top_k=None,
        top_p=None,
    )
    extracted_text = processor.decode(output[0], skip_special_tokens=True)

    # Remove prompt-related text from the output
    pattern = rf"^\s*user\s*{re.escape(prompt)}\s*assistant\s*"
    extracted_text = re.sub(pattern, "", extracted_text)
    logger.debug(f"Extracted text: {extracted_text}")

    return extracted_text
