import pytest
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from form_builder.quera_forms.enums import QuestionTypeEnum
from form_builder.quera_forms.models import Form, Question
from form_builder.users.models import User
from form_builder.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def token(db, user) -> Token:
    return Token.objects.create(user=user)


@pytest.fixture
def client(db) -> APIClient:
    return APIClient()


@pytest.fixture
def create_random_form(db, fake, user):
    def fake_form():
        created_at = fake.date_time()
        return Form.objects.create(
            title=fake.company(),
            created_at=created_at,
            created_by=user,
            updated_by=user,
            updated_at=created_at,
        )

    return fake_form


@pytest.fixture
def create_questions(db, create_random_form):
    def questions(form):
        question_number_1 = Question.objects.create(
            form=form,
            question_text="Enter number?",
            required=True,
            type=QuestionTypeEnum.NUMBER.name,
            max_value=100,
            min_value=1,
            is_decimal=False,
        )
        question_number_2 = Question.objects.create(
            form=form,
            question_text="Enter number?",
            required=True,
            type=QuestionTypeEnum.NUMBER.name,
            max_value=100,
            min_value=1,
            is_decimal=True,
        )
        question_email = Question.objects.create(
            form=form,
            question_text="Enter email?",
            required=True,
            type=QuestionTypeEnum.EMAIL.name,
        )
        question_name = Question.objects.create(
            form=form,
            question_text="what's your name?",
            required=True,
            type=QuestionTypeEnum.SHORT_TEXT.name,
            max_length=100,
        )
        question_description = Question.objects.create(
            form=form,
            question_text="description :",
            required=True,
            type=QuestionTypeEnum.LONG_TEXT.name,
            max_length=500,
        )
        return [
            question_number_1,
            question_number_2,
            question_email,
            question_name,
            question_description,
        ]

    return questions
