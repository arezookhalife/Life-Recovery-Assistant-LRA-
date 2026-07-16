from datetime import date
from django.contrib.auth.models import User
from tasks.models import Task, DailyPlan, PlannedTask

# Core MVP configuration: Max planned focus time per day (4 hours)
DAILY_CAPACITY_MINUTES = 240


def generate_daily_plan(user: User, plan_date: date = None):
    """
    Generate today's daily plan for a user.
    Selects pending tasks fitting them within DAILY_CAPACITY_MINUTES:
    1. First, includes tasks scheduled specifically for plan_date (Fixed-date tasks).
    2. Then, fills the remaining capacity with unscheduled pending tasks ordered by priority.
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

    # 1. Fetch fixed-date tasks for today (regardless of priority)
    fixed_tasks = Task.objects.filter(
        user=user,
        status="PENDING",
        scheduled_date=plan_date
    )

    # 2. Fetch flexible tasks (no scheduled date) ordered by priority
    flexible_tasks = Task.objects.filter(
        user=user,
        status="PENDING",
        scheduled_date__isnull=True
    ).order_by("-priority")

    # Combine lists: Fixed-date tasks go first
    candidate_tasks = list(fixed_tasks) + list(flexible_tasks)

    order = 1
    total_planned_minutes = 0

    for task in candidate_tasks:
        # Check if adding this task exceeds the daily capacity
        if total_planned_minutes + task.estimated_minutes > DAILY_CAPACITY_MINUTES:
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
