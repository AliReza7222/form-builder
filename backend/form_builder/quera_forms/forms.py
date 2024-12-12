from django import forms
from django.core.exceptions import ValidationError

from .factory_validators import QuestionValidatorFactory
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        validator = QuestionValidatorFactory.get_validator(
            cleaned_data.get("type")
        )

        try:
            validator.validate(cleaned_data)
        except ValidationError as e:
            for field, messages in e.message_dict.items():
                for message in messages:
                    self.add_error(field, message)

        return cleaned_data
