from rest_framework import serializers
from .models import Invitation, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(write_only=True)
    created_by = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_by_email', 'created_by', 'created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        email = validated_data.pop('created_by_email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({'created_by_email': 'User with this email does not exist'})
        validated_data['created_by'] = user
        return super().create(validated_data)

class InvitationSerializer(serializers.ModelSerializer):
    invited_by_email = serializers.EmailField(source='invited_by.email', read_only=True)
    
    class Meta:
        model = Invitation
        fields = ['id', 'task', 'email', 'invited_by', 'invited_by_email', 'status', 'created_at']
        read_only_fields = ['created_at']