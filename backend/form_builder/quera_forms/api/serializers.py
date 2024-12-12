from rest_framework import serializers

from form_builder.quera_forms.models import Form, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "question_text",
            "help_text",
            "required",
            "type",
            "max_length",
            "min_value",
            "max_value",
            "is_decimal",
        )


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = (
            "id",
            "title",
            "created_at",
            "created_by",
            "updated_by",
            "updated_at",
            "questions",
        )
