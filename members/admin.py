from django.contrib import admin

from django.contrib import admin
from .models import Task, TaskInvite

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "created_by__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(TaskInvite)
class TaskInviteAdmin(admin.ModelAdmin):
    list_display = ("task", "invitee", "invited_by", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("task__title", "invitee__username", "invited_by__username")
    ordering = ("-created_at",)
