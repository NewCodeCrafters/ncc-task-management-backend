from rest_framework import serializers
from .models import LoginLog, SignupLog
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  # ✅ Added first_name
    last_name = serializers.CharField(required=True)   # ✅ Added last_name

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']  # ✅ Included first_name & last_name

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")  # ✅ Get first_name
        last_name = validated_data.get("last_name")  # ✅ Get last_name

        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)  
        SignupLog.objects.create(user=user, first_name=first_name, last_name=last_name)  # ✅ Log signup with names

        return user







class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):  # Use "attrs" instead of "data"
        email = attrs.get("email")  # ✅ Correctly accessing email
        password = attrs.get("password")  # ✅ Correctly accessing password

        if not email or not password:
            raise serializers.ValidationError({"non_field_errors": ["Both email and password are required."]})

        user = authenticate(username=email, password=password)  # ✅ Ensure your authentication method uses "username=email"
        if user is None:
            raise serializers.ValidationError({"non_field_errors": ["Invalid credentials."]})

        attrs["user"] = user  # ✅ Store user in attrs
        return attrs  # ✅ Return attrs, not a dictionary



        
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'

        