
from django.contrib import admin
from django.urls import path

from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    
)

from .views import *


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OtpVerificationView.as_view(), name='verify_otp'),

    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('forgot_password_mail/<str:uidb64>/<str:token>/', forgot_password_mail_view, name='forgot_password_mail'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),

    path('chef_list/', ChefListView.as_view(), name='chef_list'),
    path('chef_students_list/<int:user_id>/', ChefStudentsList.as_view(), name='chef_students_list'),

    path('get_admin_user_id/', AdminDetailsView.as_view(), name='Admin_details'),
    path('get_all_chefs/', GetAllChefsAPIView.as_view(), name='get_all_chefs'),
    

    
]
