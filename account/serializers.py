from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.CharField()
class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.CharField()
    verification_code = serializers.IntegerField()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1','password2', 'gender', 'birth_date')

    def create(self, validated_data):
        password = validated_data.get('password1')
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=password,
            gender=validated_data.get('gender'),
            birth_date=validated_data.get('birth_date')
        )
        return user

    def validate(self, attrs):
       email = attrs.get('email')
       password1 = attrs.get('password1')
       password2 = attrs.get('password2')

       if not email:
           raise serializers.ValidationError('Please enter an email address.')
       try:
            EmailValidator()(email)
       except ValidationError:
           raise serializers.ValidationError('Please enter a valid email address.')

       if User.objects.filter(email=email).exists():
        raise serializers.ValidationError("This email is already registered.")
       
       if not email:
           raise serializers.ValidationError('Please enter your email.')

       if password1 != password2:
           raise serializers.ValidationError("Passwords must match.")



       return super().validate(attrs)
   
   
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User deactivated.")
                return {"user": user}  # ✅ Вернём словарь с ключом "user"
            raise serializers.ValidationError("Error login credentials.")
        raise serializers.ValidationError("Email and password required.")
