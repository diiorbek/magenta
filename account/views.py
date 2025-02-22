from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import login
from django.core.cache import cache
from .serializers import RegisterSerializer, LoginSerializer, VerifyCodeSerializer, EmailVerificationSerializer
from .utils import send_verification_email  # To'g'ri funksiya nomi ishlatilgan

class EmailVerificationView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Tasdiqlash kodini yaratish va yuborish
            verification_code = send_verification_email(email)
            
            # Tasdiqlash kodini cache-ga saqlash
            cache.set(email, verification_code, timeout=300)  # 5 daqiqaga amal qiladi
            
            return Response({"message": "Verification code sent to your email."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if not cache.get(f"verified_{email}", False):  # Default qiymat False
            return Response({"message": "Email has not been verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            cache.delete(f"verified_{email}")  # Tasdiqlash holatini o'chirish
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']
            
            cached_code = cache.get(email)
            
            if cached_code is None:
                return Response({"message": "Verification code expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)
            
            if cached_code != verification_code:
                return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
            
            cache.delete(email)
            cache.set(f"verified_{email}", True, timeout=3600)  # 1 soat amal qiladi
            
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]  # ✅ Теперь `validated_data` содержит словарь
            login(request, user)
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            if hasattr(token, 'blacklist'):
                token.blacklist()
                return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Token cannot be blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)