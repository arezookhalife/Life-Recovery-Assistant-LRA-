from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task, Disruption, RecoverySession, DailyPlan
from django.utils import timezone

class InsightsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user-insights")

    def test_insights_empty_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["today"]["completed_tasks"], 0)
        self.assertEqual(response.data["recovery"]["recovery_rate_percentage"], 0.0)

    def test_insights_with_data_and_isolation(self):
        today = timezone.localdate()
        other_user = User.objects.create_user(username="other", password="password123")

        Task.objects.create(user=self.user, title="T1", status="COMPLETED", scheduled_date=today)
        Task.objects.create(user=self.user, title="T2", status="PENDING", scheduled_date=today)

        Task.objects.create(user=other_user, title="Other T", status="COMPLETED", scheduled_date=today)

        plan = DailyPlan.objects.create(user=self.user, date=today)
        disruption = Disruption.objects.create(user=self.user, daily_plan=plan, lost_minutes=45)
        RecoverySession.objects.create(user=self.user, disruption=disruption, tasks_kept=1, tasks_moved=0, recovery_score=1.0)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["today"]["completed_tasks"], 1)
        self.assertEqual(response.data["today"]["total_tasks"], 2)
        self.assertEqual(response.data["recovery"]["disruptions_count"], 1)
        self.assertEqual(response.data["recovery"]["total_lost_minutes"], 45)
        self.assertEqual(response.data["recovery"]["recovery_rate_percentage"], 100.0)
