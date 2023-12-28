from django.urls import path
from .views import *
urlpatterns = [
    path('upload_profile_pic/', ProfileUploadView.as_view(), name='profile'),
    path('profile/', Profile.as_view(), name='profile'),
    path('update_profile/<int:profile_id>/', UpdateProfileView.as_view(), name='update-profile'),
    path('change_password/<int:user_id>/', ChangePassword.as_view(), name='change_password'),


]