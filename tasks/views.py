from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import DailyPlan
from .serializers import DailyPlanSerializer
from .services.planner import generate_daily_plan


class GenerateDailyPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        daily_plan = generate_daily_plan(user=request.user, plan_date=today)
        serializer = DailyPlanSerializer(daily_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
