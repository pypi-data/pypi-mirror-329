import logging
from typing import Optional

from transformers import AutoProcessor, Qwen2VLForConditionalGeneration, Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = ("""
You are an advanced OCR system. Transcribe the text from the image, using valid Markdown syntax (#, ##, ###,
-, *, 1., `, ```, >, ---, [ ]( ), ![ ]( ), **, ***, _, __, ~~, |, :---, ---:, :---:) to accurately capture
the style and layout. Do not include additional interpretations or explanations, and output only the text
exactly as in the image, without omissions. Replace unreadable or partially obscured text with [...].
""").replace("\n", " ").strip()


def extract_text(
    image_path: str,
    prompt: Optional[str] = None,
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct",
    max_new_tokens: int = 1024,
) -> str:
    """
    Extract text from an image using the Qwen backbone.

    Args:
        image_path (str): Path to the input image.
        prompt (Optional[str]): User-provided prompt. If None, the default prompt is used.
        model_id (str): Name or path of the Qwen2VL model.
        max_new_tokens (int): Maximum number of tokens to be generated.

    Returns:
        str: The extracted text from the image.
    """
    logger.debug(f"Starting OCR with Qwen backbone `{model_id}`.")

    # Load the model and processor
    if model_id.startswith("Qwen/Qwen2-VL"):
        model = Qwen2VLForConditionalGeneration.from_pretrained(model_id, torch_dtype="auto", device_map="auto")
    else:
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(model_id, torch_dtype="auto", device_map="auto")
    processor = AutoProcessor.from_pretrained(model_id)

    # Prepare input messages
    prompt = prompt or DEFAULT_PROMPT
    messages = [
        {"role": "user", "content": [{"type": "image", "image": image_path}, {"type": "text", "text": prompt}]},
    ]

    # Prepare inputs for the model
    formatted_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    logger.debug(f"Formatted prompt: {formatted_prompt}")
    image_inputs, _ = process_vision_info(messages)
    inputs = processor(text=[formatted_prompt], images=image_inputs, padding=True, return_tensors="pt").to(model.device)

    # Generate response
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=None,
        top_p=None,
        top_k=None,
    )
    generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
    extracted_text = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)[0]
    logger.debug(f"Extracted text:\n{extracted_text}")

    return extracted_text
