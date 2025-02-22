from django.urls import path
from .views import EmailVerificationView, VerifyEmailView, RegisterView,LoginView,LogoutView

urlpatterns = [
    path('email/verify/', EmailVerificationView.as_view(), name='email_verify'),
    path('email/confirm/', VerifyEmailView.as_view(), name='email_confirm'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="Logout"),

]