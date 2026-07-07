from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task, DailyPlan, PlannedTask


class DailyPlanGenerationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123"
        )

        self.url = "/api/daily-plan/generate/"

    def test_generate_daily_plan_selects_tasks_within_daily_capacity(self):
        self.client.force_authenticate(user=self.user)

        Task.objects.create(
            user=self.user,
            title="High Priority Task",
            priority="HIGH",
            estimated_minutes=120,
            status="PENDING",
        )

        Task.objects.create(
            user=self.user,
            title="Medium Priority Task",
            priority="HIGH",
            estimated_minutes=100,
            status="PENDING",
        )

        Task.objects.create(
            user=self.user,
            title="Low Priority Task",
            priority="LOW",
            estimated_minutes=60,
            status="PENDING",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("date", response.data)
        self.assertIn("total_estimated_minutes", response.data)
        self.assertIn("planned_tasks", response.data)

        self.assertEqual(response.data["total_estimated_minutes"], 180)
        self.assertEqual(len(response.data["planned_tasks"]), 2)

        planned_titles = [
            item["title"] for item in response.data["planned_tasks"]
        ]

        self.assertIn("Low Priority Task", planned_titles)
        self.assertIn("High Priority Task", planned_titles)
        self.assertNotIn("Medium Priority Task", planned_titles)

        self.assertEqual(
            planned_titles,
            ["Low Priority Task", "High Priority Task"]
        )

        daily_plan = DailyPlan.objects.get(
            id=response.data["id"],
            user=self.user
        )

        self.assertEqual(
            PlannedTask.objects.filter(daily_plan=daily_plan).count(),
            2
        )

    def test_generate_daily_plan_does_not_include_other_users_tasks(self):
        self.client.force_authenticate(user=self.user)

        Task.objects.create(
            user=self.other_user,
            title="Other User Task",
            priority="HIGH",
            estimated_minutes=60,
            status="PENDING",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_estimated_minutes"], 0)
        self.assertEqual(len(response.data["planned_tasks"]), 0)

    def test_generate_daily_plan_ignores_completed_tasks(self):
        self.client.force_authenticate(user=self.user)

        Task.objects.create(
            user=self.user,
            title="Completed Task",
            priority="HIGH",
            estimated_minutes=60,
            status="COMPLETED",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_estimated_minutes"], 0)
        self.assertEqual(len(response.data["planned_tasks"]), 0)
