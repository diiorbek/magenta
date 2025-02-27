from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListView, UserRetrieveUpdateDestroyView, RegisterView, LoginView
from .serializers import CustomTokenObtainPairSerializer


router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')  

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:email>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('', include(router.urls)), 
]