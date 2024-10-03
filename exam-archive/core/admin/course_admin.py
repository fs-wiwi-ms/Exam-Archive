from django import forms
from django.contrib import admin

from core.models import Course, Exam, FieldOfStudy


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 0
    fields = ["file", "year", "term"]
    readonly_fields = ["file", "year", "term"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["fields_of_study"].widget = forms.CheckboxSelectMultiple()
        self.fields["fields_of_study"].queryset = FieldOfStudy.objects.all()
        self.fields["fields_of_study"].help_text = None


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    inlines = [ExamInline]

    fieldsets = (
        (
            "Course Information",
            {
                "fields": ("title", "fields_of_study"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    list_display = ["title", "exams", "updated_at"]
    search_fields = ("title",)
    filter_horizontal = ("fields_of_study",)
    readonly_fields = ("created_at", "updated_at")

    def exams(self, obj):
        return obj.exam_set.count()

    exams.short_description = "Exams"
