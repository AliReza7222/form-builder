from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from form_builder.quera_forms.models import Form

from .serializers import FormSerializer


class FormPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class FormListView(ListAPIView):
    queryset = (
        Form.objects.all().prefetch_related("questions").order_by("created_at")
    )
    serializer_class = FormSerializer
    pagination_class = FormPagination


class FormDetailView(RetrieveAPIView):
    queryset = Form.objects.all().prefetch_related("questions")
    serializer_class = FormSerializer
