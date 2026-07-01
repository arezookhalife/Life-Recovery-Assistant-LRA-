from django.contrib import admin
from .models import Task, DailyPlan, PlannedTask, Disruption, RecoverySession

admin.site.register(Task)
admin.site.register(DailyPlan)
admin.site.register(PlannedTask)
admin.site.register(Disruption)
admin.site.register(RecoverySession)
