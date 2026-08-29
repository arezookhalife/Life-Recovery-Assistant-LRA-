from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase

from tasks.models import Task, DailyPlan, PlannedTask
from tasks.services.planner import generate_daily_plan, DAILY_CAPACITY_MINUTES


class PlannerServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="planner_user", password="password123")
        self.today = date(2026, 8, 30)

    def test_generate_daily_plan_selects_tasks_within_daily_capacity(self):
        # 3 tasks of 90 mins = 270 mins (exceeds 240 limit)
        Task.objects.create(user=self.user, title="Task 1", estimated_minutes=90, priority="HIGH")
        Task.objects.create(user=self.user, title="Task 2", estimated_minutes=90, priority="HIGH")
        Task.objects.create(user=self.user, title="Task 3", estimated_minutes=90, priority="HIGH")

        plan = generate_daily_plan(user=self.user, plan_date=self.today)

        self.assertEqual(plan.planned_tasks.count(), 2)
        total_time = sum(pt.planned_minutes for pt in plan.planned_tasks.all())
        self.assertEqual(total_time, 180)
        self.assertLessEqual(total_time, DAILY_CAPACITY_MINUTES)

    def test_generate_daily_plan_prioritizes_tasks_scheduled_for_today(self):
        # Fixed task for today (Low priority, but should be selected first)
        fixed_task = Task.objects.create(
            user=self.user,
            title="Doctor Appointment",
            estimated_minutes=60,
            priority="LOW",
            scheduled_date=self.today,
        )
        # Flexible task (High priority)
        flexible_task = Task.objects.create(
            user=self.user,
            title="Study Django",
            estimated_minutes=60,
            priority="HIGH",
            scheduled_date=None,
        )

        plan = generate_daily_plan(user=self.user, plan_date=self.today)

        planned_task_ids = list(plan.planned_tasks.order_by("order").values_list("task_id", flat=True))
        self.assertEqual(planned_task_ids[0], fixed_task.id)
        self.assertEqual(planned_task_ids[1], flexible_task.id)

    def test_generate_daily_plan_excludes_tasks_scheduled_for_other_days(self):
        tomorrow = self.today + timedelta(days=1)
        Task.objects.create(
            user=self.user,
            title="Tomorrow Task",
            estimated_minutes=60,
            scheduled_date=tomorrow,
        )
        flexible_task = Task.objects.create(
            user=self.user,
            title="Flexible Task",
            estimated_minutes=60,
            scheduled_date=None,
        )

        plan = generate_daily_plan(user=self.user, plan_date=self.today)

        planned_tasks = plan.planned_tasks.all()
        self.assertEqual(planned_tasks.count(), 1)
        self.assertEqual(planned_tasks.first().task, flexible_task)

    def test_generate_daily_plan_fills_remaining_capacity_with_flexible_tasks(self):
        # Fixed task consumes 180 mins
        Task.objects.create(
            user=self.user,
            title="Long Meeting",
            estimated_minutes=180,
            scheduled_date=self.today,
        )
        # Flexible task 1 fits in remaining 60 mins
        fit_flexible = Task.objects.create(
            user=self.user,
            title="Quick Review",
            estimated_minutes=60,
            scheduled_date=None,
        )
        # Flexible task 2 exceeds capacity (180 + 60 + 30 = 270 > 240)
        Task.objects.create(
            user=self.user,
            title="Extra Task",
            estimated_minutes=30,
            scheduled_date=None,
        )

        plan = generate_daily_plan(user=self.user, plan_date=self.today)

        planned_tasks = plan.planned_tasks.all()
        self.assertEqual(planned_tasks.count(), 2)
        total_time = sum(pt.planned_minutes for pt in planned_tasks)
        self.assertEqual(total_time, 240)
