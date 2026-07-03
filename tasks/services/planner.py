from datetime import date

from django.contrib.auth.models import User

from tasks.models import Task, DailyPlan, PlannedTask

# Core MVP configuration: Max planned focus time per day (4 hours)
DAILY_CAPACITY_MINUTES = 240


def generate_daily_plan(user: User, plan_date: date = None):
    """
    Generate today's daily plan for a user.
    Selects pending tasks ordered by priority, fitting them within
    the DAILY_CAP
    """

    if plan_date is None:
        plan_date = date.today()

    # Prevent duplicate plans for the same day
    plan, created = DailyPlan.objects.get_or_create(
        user=user,
        date=plan_date, 
    )

    if not created and plan.planned_tasks.exists():
        return plan

    # Fetch pending tasks ordered by priority (highest priority first)
    tasks = Task.objects.filter(
        user=user,
        status="PENDING"
    ).order_by("-priority")

    order = 1
    total_planned_minutes = 0

    for task in tasks:
        # Check if adding this task exceeds the daily capacity
        if total_planned_minutes + task.estimated_minutes > DAILY_CAPACITY_MINUTES:
            # If the task cannot fit, we skip it (or stop planning)
            continue

        PlannedTask.objects.create(
            daily_plan=plan,
            task=task,
            order=order,
            planned_minutes=task.estimated_minutes
        )
        
        total_planned_minutes += task.estimated_minutes
        order += 1

    return plan
