import pytest
from django.urls import reverse
from rest_framework import status

from form_builder.quera_forms.models import Answer, Response


@pytest.mark.django_db
class TestFormList:
    def test_is_authentication(self, token, client):
        url = reverse("quera_forms:forms")
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_is_not_authentication(self, client):
        url = reverse("quera_forms:forms")
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestFormDetail:
    def test_is_authentication(self, token, client, create_random_form):
        form = create_random_form()
        url = reverse("quera_forms:form_detail", kwargs={"pk": form.id})
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_is_not_authentication(self, token, client, create_random_form):
        form = create_random_form()
        url = reverse("quera_forms:form_detail", kwargs={"pk": form.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestResponseUser:
    def test_create_response_success(
        self, client, create_questions, create_random_form
    ):
        url = reverse("api:response-list")
        form = create_random_form()
        questions = create_questions(form)
        data = {
            "form": form.id,
            "user_identifier": "testuser@example.com",
            "answers": [
                {"question": questions[0].id, "answer_number": 10},
                {"question": questions[1].id, "answer_number": 10.10},
                {
                    "question": questions[2].id,
                    "answer_text": "testuser@example.com",
                },
                {"question": questions[3].id, "answer_text": "Test"},
                {"question": questions[4].id, "answer_text": "Hello world !"},
            ],
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Response.objects.count() == 1
        assert Answer.objects.count() == 5

    def test_missing_answers(
        self, client, create_questions, create_random_form
    ):
        url = reverse("api:response-list")
        form = create_random_form()
        questions = create_questions(form)
        data = {
            "form": form.id,
            "user_identifier": "testuser@example.com",
            "answers": [
                {"question": questions[0].id, "answer_number": 10},
                {"question": questions[1].id, "answer_number": 10.10},
                {
                    "question": questions[2].id,
                    "answer_text": "testuser@example.com",
                },
            ],
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "required questions have not been answered" in str(
            response.data["answers"]
        )

    def test_invalid_question_ids(
        self, client, create_questions, create_random_form
    ):
        url = reverse("api:response-list")

        form_1 = create_random_form()
        form_2 = create_random_form()

        questions_form_1 = create_questions(form_1)
        questions_form_2 = create_questions(form_2)

        data = {
            "form": form_1.id,
            "user_identifier": "testuser@example.com",
            "answers": [
                {"question": questions_form_1[0].id, "answer_number": 10},
                {"question": questions_form_1[1].id, "answer_number": 10.10},
                {
                    "question": questions_form_1[2].id,
                    "answer_text": "testuser@example.com",
                },
                {"question": questions_form_1[3].id, "answer_text": "Test"},
                {
                    "question": questions_form_2[4].id,
                    "answer_text": "Hello world !",
                },
            ],
        }

        response = client.post(url, data, format="json")

        msg_error = f"Question with ID {questions_form_2[4].id} does not belong to the specified form with ID {form_1.id}."

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert msg_error in str(response.data["answers"])

    def test_invalid_answers(
        self, client, create_questions, create_random_form
    ):
        url = reverse("api:response-list")

        form = create_random_form()
        questions = create_questions(form)
        answer_short_text = "Test" * 100
        answer_long_text = "Hello world !" * 100

        data = {
            "form": form.id,
            "user_identifier": "testuser@example.com",
            "answers": [
                {"question": questions[0].id, "answer_number": 10.10},
                {"question": questions[1].id, "answer_number": 10},
                {"question": questions[2].id, "answer_text": "testuser.com"},
                {"question": questions[3].id, "answer_text": answer_short_text},
                {"question": questions[4].id, "answer_text": answer_long_text},
            ],
        }

        response = client.post(url, data, format="json")
        response_errors = response.data.get("answers", [])

        mesg_errors = [
            f"The answer must be an integer for the question with ID {questions[0].id}.",
            f"The provided answer 'testuser.com' is not a valid email address for the question with ID {questions[2].id}.",
            f"The maximum allowed length (100 characters) for the question with ID {questions[3].id}.",
            f"The maximum allowed length (500 characters) for the question with ID {questions[4].id}.",
        ]

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        for error in mesg_errors:
            found = any(
                error in str(detail)
                for answer in response_errors
                for detail in answer.values()
            )
            assert found
