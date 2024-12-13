from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from form_builder.quera_forms.factory_validators import AnswerValidatorFactory
from form_builder.quera_forms.models import Answer, Form, Question, Response


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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "question",
            "answer_text",
            "answer_number",
        )

    def validate(self, data):
        question = data.get("question")
        if (
            question.required
            or data.get("answer_text")
            or data.get("answer_number")
        ):
            validator = AnswerValidatorFactory.get_validator(question.type)
            validator.validate(data)
        return data


class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Response
        fields = (
            "form",
            "user_identifier",
            "answers",
        )

    def validate(self, data):
        form = data.get("form")
        question_ids = {question.id for question in form.questions.all()}
        required_questions = [
            question.id for question in form.questions.filter(required=True)
        ]
        provided_answers = {
            answer.get("question").id for answer in data.get("answers")
        }

        for answer in data.get("answers"):
            if answer.get("question").id not in question_ids:
                raise serializers.ValidationError(
                    {
                        "answers": _(
                            f"Question with ID {answer.get('question').id} does not belong to the specified form with ID {form.id}."
                        )
                    }
                )

        missing_answers = set(required_questions) - provided_answers
        if missing_answers:
            missing_question_ids = ", ".join(map(str, missing_answers))
            raise serializers.ValidationError(
                {
                    "answers": _(
                        f"The following required questions have not been answered: {missing_question_ids}."
                    )
                }
            )

        return data

    def create(self, validated_data):
        answers = validated_data.pop("answers")
        response = Response.objects.create(**validated_data)
        answers_list = [
            Answer(response=response, **answer) for answer in answers
        ]
        Answer.objects.bulk_create(answers_list)
        return response
