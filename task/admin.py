from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_name', 'priority', 'status', 'assignee', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'project_name', 'assignee')

