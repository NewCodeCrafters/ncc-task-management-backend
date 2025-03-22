from django.db import models
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskInvite(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="invites")
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_invites")
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invites")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.invitee} to {self.task.title}"

