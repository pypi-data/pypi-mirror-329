import logging
from typing import Optional

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

logger = logging.getLogger(__name__)

# Default OCR prompt
DEFAULT_PROMPT = ("""
You are an advanced OCR system. Transcribe the text from the image exactly as it appears, using valid Markdown
syntax (#, ##, ###, -, *, 1., `, ```, >, ---, [ ]( ), ![ ]( ), **, ***, _, __, ~~, |, :---, ---:, :---:) to
accurately capture the style and layout. Do not add explanations, metadata, or notes beyond the exact text
itself, and ensure no part of the text is omitted. Replace unreadable or partially obscured text with [...].
""").replace("\n", " ").strip()


def extract_text(
    image_path: str,
    prompt: Optional[str] = None,
    model_id: str = "microsoft/Phi-3.5-vision-instruct",
    max_new_tokens: int = 1024,
) -> str:
    """
    Extract text from an image using the Qwen backbone.

    Args:
        image_path (str): Path to the input image.
        prompt (Optional[str]): User-provided prompt. If None, the default prompt is used.
        model_id (str): Name or path of the Phi model.
        max_new_tokens (int): Maximum number of tokens to be generated.

    Returns:
        str: The extracted text from the image.
    """
    logger.debug(f"Starting OCR with Phi backbone `{model_id}`.")

    # MPS is not supported yet
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the model and processor
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map=device,
        trust_remote_code=True,
        torch_dtype="auto",
        _attn_implementation="eager",
    )
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, num_crops=16)

    # Prepare input messages
    prompt = prompt or DEFAULT_PROMPT
    messages = [{"role": "user", "content": f"<|image_1|>\n{prompt}"}]

    # Prepare inputs for the model
    formatted_prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    logger.debug(f"Formatted prompt: {formatted_prompt}")
    image = Image.open(image_path)
    inputs = processor(formatted_prompt, [image], return_tensors="pt").to(device)

    # Generate response
    generate_ids = model.generate(
        **inputs,
        eos_token_id=processor.tokenizer.eos_token_id,
        max_new_tokens=max_new_tokens,
        do_sample=False,
    )
    generate_ids_trimmed = generate_ids[:, inputs["input_ids"].shape[1]:]
    extracted_text = processor.batch_decode(generate_ids_trimmed, skip_special_tokens=True)[0]
    logger.debug(f"Extracted text: {extracted_text}")

    return extracted_text
