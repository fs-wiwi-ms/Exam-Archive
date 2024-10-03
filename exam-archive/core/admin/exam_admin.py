from django import forms
from django.conf import settings
from django.contrib import admin

from core.models import Exam
from core.utils import get_current_term_and_year


class ExamForm(forms.ModelForm):
    EMPTY_TERM_CHOICE = [("", "---------")]

    min_year = settings.EXAM_MIN_YEAR
    max_year = settings.EXAM_MAX_YEAR
    YEARS_CHOICES = [(year, year) for year in range(min_year, max_year + 1)]
    TERM_CHOICES = [
        (term["code"], term["display_name"]) for term in settings.SEMESTER_SETTINGS
    ]

    class Meta:
        model = Exam
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_term, current_year = get_current_term_and_year()

        previous_term = self.instance.term if self.instance else None
        valid_terms = [choice[0] for choice in self.TERM_CHOICES]

        self.fields["year"].widget = forms.Select(choices=self.YEARS_CHOICES)
        self.fields["year"].initial = current_year

        if previous_term and previous_term not in valid_terms:
            self.fields["term"].widget = forms.Select(
                choices=self.EMPTY_TERM_CHOICE + self.TERM_CHOICES
            )
            self.fields["term"].help_text = "Please select a valid term."
            self.fields["term"].initial = None
        else:
            self.fields["term"].widget = forms.Select(choices=self.TERM_CHOICES)
            self.fields["term"].initial = current_term


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamForm

    fields = (
        "file",
        "year",
        "term",
        "course",
        "created_at",
        "updated_at",
    )
    list_display = (
        "file_name",
        "course",
        "file_type",
        "readable_term",
        "updated_at",
    )
    readonly_fields = ("file_name", "file_type", "created_at", "updated_at")
