from django.urls import path
from .views import GenerateDailyPlanView

urlpatterns = [
    path("daily-plan/generate/", GenerateDailyPlanView.as_view(), name="generate-daily-plan"),
]
