from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, data):
        pass


class DefaultValidator(BaseValidator):
    def validate(self, data):
        pass


class ShortTextValidator(BaseValidator):
    def validate(self, data):
        if not data.get("max_length"):
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length is required for short text questions."
                    )
                }
            )
        if data.get("max_length") > 200:
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length cannot exceed 200 characters."
                    )
                }
            )


class LongTextValidator(BaseValidator):
    def validate(self, data):
        if not data.get("max_length"):
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length is required for long text questions."
                    )
                }
            )
        if data.get("max_length") > 5000:
            raise ValidationError(
                {
                    "max_length": _(
                        "Maximum length cannot exceed 5000 characters."
                    )
                }
            )


class NumberValidator(BaseValidator):
    def validate(self, data):
        if not data.get("min_value") or not data.get("max_value"):
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
        if data.get("min_value") > data.get("max_value"):
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


class TextAnswerValidator(BaseValidator):
    def validate(self, data):
        question = data.get("question")
        if not data.get("answer_text") and question.required:
            raise serializers.ValidationError(
                {
                    "answer_text": _(
                        f"Answer text is required for the question with ID {question.id}."
                    )
                }
            )
        if len(data.get("answer_text", "")) > question.max_length:
            raise serializers.ValidationError(
                {
                    "answer_text": _(
                        f"The maximum allowed length ({question.max_length} characters) for the question with ID {question.id}."
                    )
                }
            )


class EmailAnswerValidator(BaseValidator):
    def validate(self, data):
        question = data.get("question")
        if not data.get("answer_text") and question.required:
            raise serializers.ValidationError(
                {
                    "answer_text": _(
                        f"Answer text is required for the question with ID {question.id}."
                    )
                }
            )
        try:
            validate_email(data.get("answer_text"))
        except ValidationError:
            raise serializers.ValidationError(
                {
                    "answer_text": _(
                        f"The provided answer '{data.get('answer_text')}' is not a valid email address for the question with ID {question.id}."
                    )
                }
            )


class NumberAnswerValidator(BaseValidator):
    def validate(self, data):
        answer_number = data.get("answer_number")
        question = data.get("question")

        if not answer_number and question.required:
            raise serializers.ValidationError(
                {
                    "answer_number": _(
                        f"Answer number is required for the question with ID {question.id}."
                    )
                }
            )
        if question.is_decimal and not isinstance(answer_number, float):
            raise serializers.ValidationError(
                {
                    "answer_number": _(
                        f"The answer must be a decimal number for the question with ID {question.id}."
                    )
                }
            )
        if not question.is_decimal and not answer_number.is_integer():
            raise serializers.ValidationError(
                {
                    "answer_number": _(
                        f"The answer must be an integer for the question with ID {question.id}."
                    )
                }
            )
        if answer_number > question.max_value:
            raise serializers.ValidationError(
                {
                    "answer_number": _(
                        f"The answer exceeds the maximum value ({question.max_value}) for the question with ID {question.id}."
                    )
                }
            )
        if answer_number < question.min_value:
            raise serializers.ValidationError(
                {
                    "answer_number": _(
                        f"The answer is below the minimum value ({question.min_value}) for the question with ID {question.id}."
                    )
                }
            )
