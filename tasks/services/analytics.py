from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from tasks.models import Task, Disruption, RecoverySession


def get_user_insights(user):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)  # بازه ۷ روز گذشته شامل امروز

    today_tasks = Task.objects.filter(user=user, scheduled_date=today)
    today_total = today_tasks.count()
    today_completed = today_tasks.filter(status='COMPLETED').count()

    week_tasks = Task.objects.filter(
        user=user,
        scheduled_date__range=[week_start, today]
    )
    week_total = week_tasks.count()
    week_completed = week_tasks.filter(status='COMPLETED').count()

    disruptions_qs = Disruption.objects.filter(user=user)
    recovery_sessions_qs = RecoverySession.objects.filter(user=user)

    disruptions_count = disruptions_qs.count()
    recovery_sessions_count = recovery_sessions_qs.count()
    
    total_lost_minutes = disruptions_qs.aggregate(
        total=Sum('lost_minutes')
    )['total'] or 0

    if disruptions_count > 0:
        recovery_rate = round(min(recovery_sessions_count / disruptions_count, 1.0) * 100, 1)
    else:
        recovery_rate = 0.0

    return {
        "today": {
            "completed_tasks": today_completed,
            "total_tasks": today_total,
        },
        "week": {
            "completed_tasks": week_completed,
            "total_tasks": week_total,
        },
        "recovery": {
            "disruptions_count": disruptions_count,
            "recovery_sessions_count": recovery_sessions_count,
            "total_lost_minutes": total_lost_minutes,
            "recovery_rate_percentage": recovery_rate,
        }
    }
