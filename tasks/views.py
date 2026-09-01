from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyPlan, Task, Disruption
from .serializers import DailyPlanSerializer, TaskSerializer, DisruptionSerializer
from .services.planner import generate_daily_plan


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class GenerateDailyPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        daily_plan = generate_daily_plan(user=request.user, plan_date=today)
        serializer = DailyPlanSerializer(daily_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DisruptionCreateView(generics.CreateAPIView):
    serializer_class = DisruptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)