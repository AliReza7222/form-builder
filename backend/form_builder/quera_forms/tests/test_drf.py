import pytest
from django.urls import reverse
from rest_framework import status


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
