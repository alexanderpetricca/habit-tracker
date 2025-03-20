from django.contrib import admin

from habits.models import Habit, CompletedDay


admin.site.register(Habit)
admin.site.register(CompletedDay)
