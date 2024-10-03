from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile

from core.utils import extract_file_extension, extract_file_mime_type


def validate_term(value) -> None:
    """
    Validator to ensure that the 'term' field has a valid value based on SEMESTER_SETTINGS.
    """
    valid_terms = [term["code"] for term in settings.SEMESTER_SETTINGS]

    if value not in valid_terms:
        raise ValidationError(
            f"Invalid term '{value}'. Allowed terms: {', '.join(valid_terms)}"
        )


def validate_year(value) -> None:
    """
    Validator to ensure the year is within a valid range, e.g., between 2000 and the current year.
    """
    min_year = settings.EXAM_MIN_YEAR
    max_year = settings.EXAM_MAX_YEAR

    if not (min_year <= value <= max_year):
        raise ValidationError(
            f"Year must be between {min_year} and {max_year}. Provided year: {value}"
        )


def validate_file(file: FieldFile) -> None:
    """
    Validates both the file extension, MIME type, and file size of the uploaded file.
    The allowed formats and MIME types are fetched from settings.
    """
    allowed_formats: dict[str, dict] = {
        f["extension"]: f for f in settings.FILE_UPLOAD_ALLOWED_FORMATS
    }

    file_extension: str = extract_file_extension(file)
    file_mime_type: str = extract_file_mime_type(file)

    if not file_extension or not file_mime_type:
        raise ValidationError(f"The selected file '{file.name}' does not exist.")

    # Validate file extension exists in allowed formats
    if file_extension not in allowed_formats.keys():
        raise ValidationError(
            f"Unsupported file extension: {file_extension}. Allowed extensions are: {', '.join(allowed_formats.keys())}"
        )

    # Validate MIME type matches the expected MIME type for the file extension
    expected_mime_type: str = allowed_formats[file_extension]["mime_type"]
    if file_mime_type != expected_mime_type:
        raise ValidationError(
            f"File MIME type '{file_mime_type}' does not match the expected MIME type '{expected_mime_type}' for extension '{file_extension}'."
        )

    # Validate file size using the max_size defined for the file type
    max_file_size: int = allowed_formats[file_extension]["max_size"]
    if file.size > max_file_size:
        raise ValidationError(
            f"File size exceeds the limit of {allowed_formats[file_extension]['max_size_mb']} MB."
        )
