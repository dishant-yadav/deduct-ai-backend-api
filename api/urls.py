from django.urls import path, include
from .views import (
    TestView,
    CreateCase,
    # CaseViewSet,
    EvidencePrecautionProcedureView,
    CaseSectionView,
    SuspectSupportingDocView,
)

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"cases", CaseViewSet, basename="cases")


urlpatterns = [
    path("test", TestView.as_view()),
    path("case_create", CreateCase.as_view()),
    path("evidences/<uuid:pk>/", EvidencePrecautionProcedureView.as_view()),
    path("sections/<uuid:pk>/", CaseSectionView.as_view()),
    path("suspects/<uuid:pk>/", SuspectSupportingDocView.as_view()),
    # path("", include(router.urls)),
]
