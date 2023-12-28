from rest_framework import serializers
from .models import Course, Category, CourseVideos, User
from payment.models import Payment




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'category_image']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'image', 'username']

class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideos
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideos
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ChefEarningsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()
    class Meta:
        model = Payment
        fields = ['course', 'user', 'amount', 'payment_date']