from django.db import models
from users.models import User
from course.models import Course
from django.utils import timezone

# Create your models here.

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chef_payments', limit_choices_to={'is_chef': True})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payed = models.BooleanField(default=False)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s payment for {self.course.title}"
