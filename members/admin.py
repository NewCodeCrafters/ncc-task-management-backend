from django.contrib import admin

from django.contrib import admin
from .models import Task, Invitation

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('task', 'email', 'invited_by', 'status', 'created_at')

