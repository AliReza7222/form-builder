from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from form_builder.quera_forms.models import Form, Response

from .serializers import FormSerializer, ResponseSerializer


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


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    http_method_names = ("post", "put", "patch")
    permission_classes = (AllowAny,)
