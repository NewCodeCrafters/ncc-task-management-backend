from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils.timezone import now
from django.conf import settings

class SignupLog(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    signup_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signup - {self.user.username} ({self.user_defined_id})"

class LoginLog(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)


    def __str__(self):
        return f"Login - {self.user.username} at {self.login_time}"
