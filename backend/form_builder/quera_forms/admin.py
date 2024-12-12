from django.contrib import admin

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
    list_display = ("title", "created_at")
    search_fields = ("title",)
    inlines = [QuestionInline]
