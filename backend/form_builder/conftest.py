import pytest
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from form_builder.quera_forms.models import Form
from form_builder.users.models import User


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def create_random_user(fake: Faker, django_user_model: User):
    def fake_user():
        return django_user_model.objects.create_user(
            username=fake.user_name(), password="password12345", is_staff=True
        )

    return fake_user


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def token(db, create_random_user) -> Token:
    user = create_random_user()
    return Token.objects.create(user=user)


@pytest.fixture
def client(db) -> APIClient:
    return APIClient()


@pytest.fixture
def create_random_form(db, fake, create_random_user):
    def fake_form():
        created_by = create_random_user()
        created_at = fake.date_time()
        return Form.objects.create(
            title=fake.company(),
            created_at=created_at,
            created_by=created_by,
            updated_by=created_by,
            updated_at=created_at,
        )

    return fake_form
