from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=123,blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    is_chef = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True) 
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        if self.name is not None:
            return self.name
        return self.username  
