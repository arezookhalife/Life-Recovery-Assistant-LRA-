from django.urls import path
from .views import GenerateDailyPlanView, TaskDetailView, TaskListCreateView, DisruptionCreateView, QuickRecoveryView, UserInsightsView  

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("daily-plan/generate/", GenerateDailyPlanView.as_view(), name="generate-daily-plan"),
    path('disruptions/', DisruptionCreateView.as_view(), name='disruption-create'),
    path('recoveries/quick-reset/', QuickRecoveryView.as_view(), name='quick-recovery'),
    path("insights/", UserInsightsView.as_view(), name="user-insights"),
]
