from datetime import date

from django.contrib.auth.models import User

from tasks.models import Task, DailyPlan, PlannedTask


def generate_daily_plan(user: User):
    """
    Generate today's daily plan for a user
    based on pending tasks.
    """

    today = date.today()

    # Prevent duplicate plans for the same day
    plan, created = DailyPlan.objects.get_or_create(
        user=user,
        date=today
    )

    if not created:
        return plan

    # Fetch pending tasks ordered by priority
    tasks = Task.objects.filter(
        user=user,
        status="PENDING"
    ).order_by("-priority")

    order = 1

    for task in tasks:
        PlannedTask.objects.create(
            daily_plan=plan,
            task=task,
            order=order,
            planned_minutes=task.estimated_minutes
        )

        order += 1

    return plan
