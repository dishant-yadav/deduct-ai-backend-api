from django.urls import path
from .views import PrecautionsView

urlpatterns = [
    path("", PrecautionsView.as_view()),
]
