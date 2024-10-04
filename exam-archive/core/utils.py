import datetime
from typing import Tuple

import magic
from django.conf import settings
from django.db.models.fields.files import FieldFile


def extract_file_extension(file: FieldFile) -> str:
    return f".{file.name.split(".")[-1].lower()}"


def extract_file_mime_type(file: FieldFile) -> str:
    file_mime_type: str = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    return file_mime_type


def to_snake_case(s: str) -> str:
    return s.casefold().replace(" ", "_")


def get_current_term_and_year() -> Tuple[str, str]:
    today = datetime.date.today()
    current_year = today.year
    current_month_day = (today.month, today.day)

    for term in settings.TERMS:
        start_month_day = term["start_date"]
        end_month_day = term["end_date"]

        if start_month_day[0] > end_month_day[0]:
            if (
                start_month_day <= current_month_day
                or current_month_day <= end_month_day
            ):
                return (
                    term["code"],
                    current_year
                    if current_month_day >= start_month_day
                    else current_year - 1,
                )
        else:
            if start_month_day <= current_month_day <= end_month_day:
                return term["code"], current_year

    return None, None
