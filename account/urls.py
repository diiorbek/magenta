from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView


router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')  

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)), 
]