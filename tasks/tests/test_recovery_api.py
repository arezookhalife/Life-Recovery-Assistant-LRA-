from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import DailyPlan, Disruption, PlannedTask, RecoverySession, Task


class QuickRecoveryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        self.daily_plan = DailyPlan.objects.create(user=self.user, date=date.today())
        self.task = Task.objects.create(
            user=self.user,
            title="Read Django Documentation",
            estimated_minutes =60,
            first_tiny_step="Read only the introduction page",
        )
        PlannedTask.objects.create(
            daily_plan=self.daily_plan,
            task=self.task,
            order=1,
            planned_minutes=60,
        )
        self.disruption = Disruption.objects.create(
            user=self.user,
            daily_plan=self.daily_plan,
            lost_minutes=30,
            reason="Got distracted",
        )
        self.url = reverse("quick-recovery")

    def test_quick_recovery_returns_next_tiny_step(self):
        payload = {
            "disruption": self.disruption.id,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecoverySession.objects.count(), 1)
        self.assertIn("first_tiny_step", response.data)
        self.assertEqual(response.data["first_tiny_step"], "Read only the introduction page")
        self.assertEqual(response.data["next_task_title"], "Read Django Documentation")
