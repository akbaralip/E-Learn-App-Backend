from django.db import models
from users.models import User

# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='category_image/', blank=True, null=True)

    def __str__(self):
        return self.category


class Course(models.Model):
    title = models.CharField(max_length=255)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=500)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    demo_video = models.FileField(upload_to='course_videos/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cover_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    is_listed = models.BooleanField(default=False)
    

    
    def __str__(self):
        return self.title

class CourseVideos(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True , null=True)
    videos = models.FileField(upload_to='course_videos/', blank=True, null=True)
    description = models.TextField()
    title = models.CharField(max_length=255, default=("Default Title"))

    def __str__(self):
        return f"{self.course.title} - Video {self.id}"
