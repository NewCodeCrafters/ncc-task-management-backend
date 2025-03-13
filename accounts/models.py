from django.db import models
import uuid
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    signup_time = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)  # ✅ Added first name
    last_name = models.CharField(max_length=50, blank=True, null=True)   # ✅ Added last name

    def __str__(self):
        return f"Signup - {self.first_name} {self.last_name} ({self.users_id})"

class LoginLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    first_name = models.CharField(max_length=50, blank=True, null=True)  # ✅ Added first name
    last_name = models.CharField(max_length=50, blank=True, null=True)   # ✅ Added last name

    def __str__(self):
        return f"Login - {self.first_name} {self.last_name} at {self.login_time}"
