from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import DailyPlan, Disruption


class DisruptionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.daily_plan = DailyPlan.objects.create(user=self.user, date=date(2026, 8, 30))
        self.url = reverse("disruption-create")

    def test_log_disruption_successfully(self):
        payload = {
            "daily_plan": self.daily_plan.id,
            "lost_minutes": 45,
            "reason": "Social media distraction",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Disruption.objects.count(), 1)
        disruption = Disruption.objects.first()
        self.assertEqual(disruption.user, self.user)
        self.assertEqual(disruption.daily_plan, self.daily_plan)
        self.assertEqual(disruption.lost_minutes, 45)
        self.assertEqual(disruption.reason, "Social media distraction")
