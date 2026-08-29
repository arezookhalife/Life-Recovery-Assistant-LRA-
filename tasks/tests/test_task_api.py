from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.list_create_url = reverse("task-list-create")

    def test_create_task_with_behavioral_fields_and_scheduled_date(self):
        payload = {
            "title": "Finish report draft",
            "priority": "HIGH",
            "estimated_minutes": 60,
            "scheduled_date": "2026-08-30",
            "first_tiny_step": "Open the doc template",
            "good_enough_definition": "Outline introduction and 2 main sections",
        }

        response = self.client.post(self.list_create_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.title, payload["title"])
        self.assertEqual(str(task.scheduled_date), payload["scheduled_date"])
        self.assertEqual(task.first_tiny_step, payload["first_tiny_step"])
        self.assertEqual(task.good_enough_definition, payload["good_enough_definition"])
        self.assertEqual(task.postpone_count, 0)

    def test_list_tasks_only_returns_authenticated_user_tasks(self):
        Task.objects.create(user=self.user, title="My Task", estimated_minutes=30)
        Task.objects.create(user=self.other_user, title="Other User Task", estimated_minutes=45)

        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "My Task")

    def test_update_task_scheduled_date_and_details(self):
        task = Task.objects.create(
            user=self.user,
            title="Initial Title",
            estimated_minutes=30,
            scheduled_date=date(2026, 8, 30),
        )
        detail_url = reverse("task-detail", kwargs={"pk": task.id})

        payload = {
            "title": "Updated Title",
            "scheduled_date": "2026-08-31",
        }
        response = self.client.patch(detail_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Title")
        self.assertEqual(str(task.scheduled_date), "2026-08-31")

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, title="Task to delete", estimated_minutes=20)
        detail_url = reverse("task-detail", kwargs={"pk": task.id})

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
