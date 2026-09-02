from tasks.models import PlannedTask, RecoverySession


def perform_quick_recovery(disruption, user):
    daily_plan = disruption.daily_plan

    first_planned = (
        PlannedTask.objects.filter(daily_plan=daily_plan)
        .select_related("task")
        .order_by("order")
        .first()
    )

    next_task_title = (
        first_planned.task.title
        if first_planned
        else "No planned tasks found"
    )
    first_tiny_step = (
        first_planned.task.first_tiny_step
        if first_planned and first_planned.task.first_tiny_step
        else "Start with 2 minutes on the first task"
    )

    # ایجاد نشست بازیابی مطابق با فیلدهای واقعی مدل
    session = RecoverySession.objects.create(
        user=user,
        disruption=disruption,
        tasks_kept=1,
        tasks_moved=0,
        recovery_score=100.0,
    )

    return {
        "recovery_session_id": session.id,
        "next_task_title": next_task_title,
        "first_tiny_step": first_tiny_step,
    }
