from django.urls import path

from .views import FormDetailView, FormListView

urlpatterns = [
    path("forms/", FormListView.as_view(), name="forms"),
    path("form/<int:pk>/", FormDetailView.as_view(), name="form_detail"),
]
