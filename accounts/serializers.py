from rest_framework import serializers
from django.contrib.auth.models import User

class SignupSerializer(serializers.ModelSerializer):
    user_defined_id = serializers.UUIDField(read_only=True)  # Auto-generated ID

    class Meta:
        model = User
        fields =  '__all__'
        extra_kwargs = {"password": {"write_only": True}}  # Hide password in responses

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],  # Using email as username
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        

        SignupLog.objects.create(user=user)

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(username=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        