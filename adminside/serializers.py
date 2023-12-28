from rest_framework import serializers
from payment.models import Payment
from users.models import User
from course.models import Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'image', 'is_chef', 'is_admin', 'otp', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Payment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'