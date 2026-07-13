from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    estimated_minutes = models.PositiveIntegerField(default=30)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    scheduled_date = models.DateField(null=True, blank=True, help_text="Specific date for the task.")
    first_tiny_step = models.CharField(max_length=255, null=True, blank=True, help_text="The smallest step to start.")
    good_enough_definition = models.CharField(max_length=255, null=True, blank=True, help_text="Minimum acceptable result.")
    postpone_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DailyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class PlannedTask(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('SKIPPED', 'Skipped'),
    ]

    daily_plan = models.ForeignKey(
        DailyPlan,
        on_delete=models.CASCADE,
        related_name='planned_tasks'
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    planned_minutes = models.PositiveIntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"{self.task.title} ({self.daily_plan.date})"


class Disruption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daily_plan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    lost_minutes = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Disruption - {self.lost_minutes} minutes"


class RecoverySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disruption = models.ForeignKey(Disruption, on_delete=models.CASCADE)
    tasks_kept = models.PositiveIntegerField()
    tasks_moved = models.PositiveIntegerField()
    recovery_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recovery {self.id} - Score {self.recovery_score}"
