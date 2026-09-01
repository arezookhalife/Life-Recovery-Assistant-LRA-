from rest_framework import serializers
from .models import DailyPlan, PlannedTask, Task, Disruption  


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "priority",
            "estimated_minutes",
            "scheduled_date",
            "first_tiny_step",
            "good_enough_definition",
            "postpone_count",
            "status",
        ]
        read_only_fields = ["id", "postpone_count"]

        
class PlannedTaskSerializer(serializers.ModelSerializer):
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
        return sum(pt.task.estimated_minutes for pt in obj.planned_tasks.all())
    


class DisruptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disruption
        fields = [
            "id",
            "daily_plan",
            "lost_minutes",
            "reason",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]    