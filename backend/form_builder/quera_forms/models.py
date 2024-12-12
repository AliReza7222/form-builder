from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .enums import QuestionTypeEnum

User = get_user_model()


class Form(models.Model):
    title = models.CharField(  # type: ignore
        max_length=100, verbose_name=_("Title"), unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore
    created_by = models.ForeignKey(  # type: ignore
        User,
        on_delete=models.CASCADE,
        related_name="created_by",
        verbose_name=_("Created By"),
    )
    updated_by = models.ForeignKey(  # type: ignore
        User,
        on_delete=models.CASCADE,
        related_name="updated_by",
        verbose_name=_("Updated By"),
    )
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=["title"], name="form_title_idx")]


class Question(models.Model):
    form = models.ForeignKey(  # type: ignore
        Form,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Form"),
    )
    question_text = models.CharField(  # type: ignore
        max_length=250, verbose_name=_("Question Text")
    )
    help_text = models.CharField(_("Help text"), blank=True, max_length=250)  # type: ignore
    required = models.BooleanField(default=True, verbose_name=_("Required"))  # type: ignore
    type = models.CharField(  # type: ignore
        max_length=50,
        choices=QuestionTypeEnum.choices(),
        verbose_name=_("Type"),
    )
    max_length = models.PositiveIntegerField(  # type: ignore
        null=True, blank=True, verbose_name=_("Maximum Length")
    )
    min_value = models.FloatField(  # type: ignore
        null=True, blank=True, verbose_name=_("Minimum Value")
    )
    max_value = models.FloatField(  # type: ignore
        null=True, blank=True, verbose_name=_("Maximum Value")
    )
    is_decimal = models.BooleanField(  # type: ignore
        null=True, blank=True, verbose_name=_("Is Decimal"), default=False
    )

    def __str__(self) -> str:
        return f"{self.form} | {self.type}"

    class Meta:
        indexes = [models.Index(fields=["type"], name="question_type_idx")]


class Answer(models.Model):
    question = models.ForeignKey(  # type: ignore
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Question"),
    )
    user = models.ForeignKey(  # type: ignore
        User,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name=_("User"),
    )
    answer_text = models.TextField(  # type: ignore
        blank=True, null=True, verbose_name=_("Answer")
    )
