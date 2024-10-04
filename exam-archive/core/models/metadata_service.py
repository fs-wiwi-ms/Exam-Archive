import logging
from collections.abc import Callable

from django.conf import settings
from django.db.models.fields.files import FieldFile
from docx import Document
from pypdf import PdfReader, PdfWriter

from core.utils import extract_file_mime_type

logger = logging.getLogger(__name__)


def modify_file_metadata(file: FieldFile) -> None:
    """Modifies the metadata of the file in-place based on file type."""

    file_mime_type: str = extract_file_mime_type(file)

    file_handlers: dict[str, Callable] = {
        "application/pdf": _process_pdf,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": _process_docx,
        # Future file types can be added here
    }
    file_handler: Callable[[FieldFile], None] = file_handlers.get(file_mime_type)

    if file_handler:
        file_handler(file)
    else:
        logger.warning(
            f"File type '{file_mime_type}' not supported for metadata modification."
        )


def _process_pdf(file_field: FieldFile) -> None:
    """Processes PDF files to modify the Author metadata and overwrite the original file."""

    logger.info(
        f"Starting the process of updating PDF metadata for file: '{file_field.name}'."
    )
    try:
        with file_field.open("rb") as pdf_file:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            # Copy the content to the new PDF
            writer.append_pages_from_reader(reader)

            # Set the Author
            author: str = settings.EXAM_METADATA_AUTHOR
            writer.add_metadata({"/Author": author})

        with file_field.open("wb") as pdf_output_file:
            writer.write(pdf_output_file)

        logger.info(
            f"Successfully processed and updated PDF metadata for file '{file_field.name}'."
        )

    except Exception as e:
        logger.error(
            f"An error occurred while processing the PDF file '{file_field.name}': {e}",
            exc_info=True,
        )


def _process_docx(file_field: FieldFile) -> None:
    """Processes DOCX files to modify the Author metadata and overwrite the original file."""

    logger.info(
        f"Starting the process of updating DOCX metadata for file: '{file_field.name}'."
    )
    try:
        with file_field.open("rb") as docx_file:
            document = Document(docx_file)
            # Assuming metadata modification via core properties
            core_props = document.core_properties
            core_props.author = settings.EXAM_METADATA_AUTHOR
            document.add_paragraph("It was a dark and stormy night.")

        with file_field.open("wb") as docx_output_file:
            document.save(docx_output_file)

        logger.info(
            f"Successfully processed and updated DOCX metadata for file '{file_field.name}'."
        )

    except Exception as e:
        logger.error(
            f"An error occurred while processing the DOCX file '{file_field.name}': {e}",
            exc_info=True,
        )
