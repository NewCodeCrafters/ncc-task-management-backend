from rest_framework import serializers
from .models import Task, TaskInvite
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Task, TaskInvite


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class TaskInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInvite
        fields = "__all__"
