from django.contrib import admin

from core.models import DegreeType, FieldOfStudy


@admin.register(DegreeType)
class DegreeTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "degree")
    search_fields = ("name", "abbreviation")
    list_filter = ("degree",)
