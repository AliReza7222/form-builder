from django.contrib import admin

from .enums import TabFormAdminPanel
from .fields import *
from .forms import QuestionForm
from .models import Form, Question


class QuestionInline(admin.StackedInline):
    model = Question
    form = QuestionForm
    extra = 0

    class Media:
        js = ("js/questions_admin.js",)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = FORM_DISPLAY_FIELDS
    search_fields = FORM_SEARCH_FIELDS
    readonly_fields = FORM_READONLY_FIELDS
    inlines = [QuestionInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (TabFormAdminPanel.GENERAL.value, {"fields": FORM_GENERAL_FIELDS}),
        )
        if obj:
            fieldsets += (
                (
                    TabFormAdminPanel.INFO.value,
                    {"fields": FORM_READONLY_FIELDS},
                ),
            )
        return fieldsets

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user == obj.created_by or request.user.is_superuser
        super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
