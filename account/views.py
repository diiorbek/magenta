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

from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
)

User = get_user_model()

@extend_schema(tags=["Registration"])
class LoginView(APIView):
    serializer_class = LoginSerializer  

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
            400: "Bad Request"
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Registration"])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["Registration"],
        operation_summary="User registration",
        operation_description="Register a new user with email and password."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema(tags=["Registration"])
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None  

    @swagger_auto_schema(
        tags=["Registration"],
        operation_summary="List users",
        operation_description="Retrieve a list of all registered users."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@extend_schema(tags=["Registration"])
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'  

    @swagger_auto_schema(
        tags=["Registration"],
        operation_summary="Get user details",
        operation_description="Retrieve user details by email."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Registration"],
        operation_summary="Update user",
        operation_description="Update user details by email."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Registration"],
        operation_summary="Delete user",
        operation_description="Delete a user by email.",
        responses={200: openapi.Response("User deleted successfully")}
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

@extend_schema(tags=["Registration"])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Registration"],
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response("Password updated successfully", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Password updated successfully")
                }
            )),
            400: "Bad Request"
        },
        operation_summary="Change user password",
        operation_description="Allows an authenticated user to change their password.",
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
