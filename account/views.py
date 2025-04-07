from rest_framework import generics, viewsets
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
) 
 
User = get_user_model()

@extend_schema(tags=["Registration"])
class LoginView(APIView):
    serializer_class = LoginSerializer  
    permission_classes = []  # ✅ Отключаем проверку прав
    authentication_classes = []  # ✅ Отключаем JWT, Basic и Session для логина

    @swagger_auto_schema(
        tags=["Registration"],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Login successful", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Login successful"),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="your_refresh_token"),
                    "access": openapi.Schema(type=openapi.TYPE_STRING, example="your_access_token"),
                }
            )),
        },
        operation_summary="User login",
        operation_description="Authenticate a user and return JWT tokens."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({
            "message": "Login accepted, but credentials are incorrect",
            "refresh": None,
            "access": None,
        }, status=status.HTTP_200_OK)   
        
    