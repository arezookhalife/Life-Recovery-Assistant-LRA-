from rest_framework import serializers
from .models import DailyPlan, PlannedTask


class PlannedTaskSerializer(serializers.ModelSerializer):
    # برای این که اطلاعات خودِ Task (مثل عنوان و اولویت) را در خروجی داشته باشیم:
    task_id = serializers.IntegerField(source="task.id", read_only=True)
    title = serializers.CharField(source="task.title", read_only=True)
    priority = serializers.CharField(source="task.priority", read_only=True)
    estimated_minutes = serializers.IntegerField(source="task.estimated_minutes", read_only=True)

    class Meta:
        model = PlannedTask
        fields = ["task_id", "title", "priority", "estimated_minutes", "order"]


class DailyPlanSerializer(serializers.ModelSerializer):
   
    total_estimated_minutes = serializers.SerializerMethodField()
    planned_tasks = PlannedTaskSerializer(many=True, read_only=True)

    class Meta:
        model = DailyPlan
        fields = ["id", "date", "total_estimated_minutes", "planned_tasks"]


    def get_total_estimated_minutes(self, obj):
        return sum(task.planned_minutes for task in obj.planned_tasks.all())