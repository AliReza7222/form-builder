from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from form_builder.quera_forms.api.views import ResponseViewSet
from form_builder.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("response", ResponseViewSet, basename="response")

app_name = "api"
urlpatterns = router.urls
