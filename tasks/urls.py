from django.urls import path
from .views import GenerateDailyPlanView, TaskDetailView, TaskListCreateView, DisruptionCreateView, QuickRecoveryView, UserInsightsView,RegisterView, CurrentUserView  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    # Auth Endpoints
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", CurrentUserView.as_view(), name="auth-me"),

    # Task Endpoints
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

    # Daily Plan & Recovery Endpoints
    path("daily-plan/generate/", GenerateDailyPlanView.as_view(), name="generate-daily-plan"),
    path('disruptions/', DisruptionCreateView.as_view(), name='disruption-create'),
    path('recoveries/quick-reset/', QuickRecoveryView.as_view(), name='quick-recovery'),

    # Insights / Analytics
    path("insights/", UserInsightsView.as_view(), name="user-insights"),
]
