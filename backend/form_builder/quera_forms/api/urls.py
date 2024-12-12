from django.urls import path

from .views import FormListView

urlpatterns = [
    path("forms/", FormListView.as_view(), name="forms"),
]
