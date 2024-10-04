from django.conf import settings
from django.db import models

from core.models.metadata_service import modify_file_metadata
from core.models.validators import validate_file, validate_term, validate_year
from core.utils import extract_file_extension, to_snake_case


class Exam(models.Model):
    file = models.FileField(upload_to="exams/", validators=[validate_file])
    year = models.PositiveIntegerField(
        validators=[validate_year], help_text="The year the term started."
    )
    term = models.CharField(max_length=2, validators=[validate_term])
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def file_name(self):
        file_extension: str = extract_file_extension(self.file)
        return f"{to_snake_case(str(self.course))}-{self.readable_term}{file_extension}"

    @property
    def readable_term(self):
        for term in settings.TERMS:
            if term["code"] == self.term:
                start_month, _ = term["start_date"]
                end_month, _ = term["end_date"]
                if start_month > end_month:
                    return f"{term['code']}-{self.year}/{str(self.year + 1)[-2:]}"
                else:
                    return f"{term['code']}-{self.year}"

        return "Unknown Term"

    @property
    def file_type(self):
        file_extension: str = extract_file_extension(self.file)

        display_names: dict[str, str] = {
            file_format["extension"]: file_format["display_name"]
            for file_format in settings.EXAM_FILE_FORMATS
        }

        return display_names.get(file_extension, "Unknown")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        modify_file_metadata(self.file)

    def __str__(self) -> str:
        return self.file_name
