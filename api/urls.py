from django.urls import path, include
from .views import TestView, FileUploadView, CaseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"cases", CaseViewSet, basename="cases")


urlpatterns = [
    path("test", TestView),
    path("file", FileUploadView.as_view()),
    path("", include(router.urls)),
]
