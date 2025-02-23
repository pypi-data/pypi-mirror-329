import logging

import pypandoc

logger = logging.getLogger(__name__)


def merge(texts: list[str]) -> str:
    """
    Merge multiple Markdown texts into a single document.

    Args:
        texts (list[str]): List of Markdown content strings.

    Returns:
        str: Combined Markdown content as a single string.
    """
    logger.debug("Merging multiple Markdown texts into a single document.")
    return "\n\n".join(texts)


def export_txt(md_content: str, output_path: str) -> None:
    """
    Convert Markdown content to plain text and save to a file.

    Args:
        md_content (str): Markdown content to convert.
        output_path (str): File path to save the plain text output.
    """
    logger.debug(f"Converting Markdown to plain text and saving to `{output_path}`.")
    plain_text = pypandoc.convert_text(md_content, to="plain", format="markdown")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(plain_text)


def export_docx(md_content: str, output_path: str) -> None:
    """
    Convert Markdown content to docx format and save to a file.

    Args:
        md_content (str): Markdown content to convert.
        output_path (str): File path to save the docx output.
    """
    logger.debug(f"Converting Markdown to DOCX format and saving to `{output_path}`.")
    pypandoc.convert_text(md_content, to="docx", format="markdown", outputfile=output_path)


def export_md(md_content: str, output_path: str) -> None:
    """
    Save Markdown content to a file.

    Args:
        md_content (str): Markdown content to save.
        output_path (str): File path to save the Markdown content.
    """
    logger.debug(f"Saving Markdown content to `{output_path}`.")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(md_content)


def export_pdf(md_content: str, output_path: str) -> None:
    """
    Convert Markdown content to PDF format and save to a file.

    Args:
        md_content (str): Markdown content to convert.
        output_path (str): File path to save the PDF output.
    """
    logger.debug(f"Converting Markdown to PDF format and saving to `{output_path}`.")
    pypandoc.convert_text(
        md_content, to="pdf",
        format="markdown",
        outputfile=output_path,
        extra_args=["--pdf-engine=xelatex", "-Vgeometry:margin=1in", "-Vpagestyle=empty"]
    )
