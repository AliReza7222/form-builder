from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class QuestionValidator(ABC):
    @abstractmethod
    def validate(self, cleaned_data):
        pass


class DefaultValidator(QuestionValidator):
    def validate(self, cleaned_data):
        pass


class ShortTextValidator(QuestionValidator):
    def validate(self, cleaned_data):
        if not cleaned_data.get("max_length"):
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length is required for short text questions."
                    )
                }
            )
        if cleaned_data.get("max_length") > 200:
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length cannot exceed 200 characters."
                    )
                }
            )


class LongTextValidator(QuestionValidator):
    def validate(self, cleaned_data):
        if not cleaned_data.get("max_length"):
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length is required for long text questions."
                    )
                }
            )
        if cleaned_data.get("max_length") > 5000:
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length cannot exceed 5000 characters."
                    )
                }
            )


class NumberValidator(QuestionValidator):
    def validate(self, cleaned_data):
        if not cleaned_data.get("min_value") or not cleaned_data.get(
            "max_value"
        ):
            raise ValidationError(
                {
                    "min_value": _(
                        "Minimum value is required for number questions."
                    ),
                    "max_value": _(
                        "Maximum value is required for number questions."
                    ),
                }
            )
        if cleaned_data.get("min_value") > cleaned_data.get("max_value"):
            raise ValidationError(
                {
                    "min_value": _(
                        "Minimum value cannot be greater than maximum value."
                    ),
                    "max_value": _(
                        "Maximum value cannot be less than minimum value."
                    ),
                }
            )
