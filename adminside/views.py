from django.shortcuts import render
from rest_framework.views import APIView
from users.serializers import UserListSerializer
from rest_framework.response import Response
from users.models import User
from course.models import Category
from rest_framework import status
from backend import settings
from django.core.mail import send_mail 
from payment.models import Payment
from django.db.models import Sum
from .serializers import *

# Create your views here.
class UserListView(APIView):
    def get(self, request):
        userlist = User.objects.filter(is_superuser=False, is_chef=False).order_by('username')
        serializer = UserListSerializer({'userlist': userlist})
        return Response(serializer.data)


    
class BlockUser(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()

            if user.is_chef:
                subject = 'Account Deactivated'
                message = f'Hello {user.username},\nYour account has been deactivated. You can no longer log in with your username and password.'
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

            return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnBlockUser(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if not user.is_active:
                # Unblock the user
                user.is_active = True
                user.save()
                if user.is_chef:
                    subject = 'Account activated'
                    message = f'Hello {user.username},\nYour account has been activated,\n Now you can login with your username and password.'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                return Response({'message': 'User Unblocked successfully'}, status=status.HTTP_200_OK)
            else:
                print('=====+++++++=====')
                return Response({"message": "User is already active"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ChefsListView(APIView):
    def get(self, request):
        try:
            userlist = User.objects.filter(is_chef=True).order_by('username')
            serializer = UserListSerializer({'userlist': userlist})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TotalRevenueView(APIView):
    def get(self, request):
        total_revenue = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({'totalRevenue':total_revenue})



class AllTransactionsView(APIView):
    def get(self, request):
        transactions = Payment.objects.all()
        serialized_transactions = PaymentSerializer(transactions, many=True)
        transactions_count = transactions.count()
        serialized_data_with_count = {
            'transactions': serialized_transactions.data,
            'transactions_count': transactions_count,
        }
        return Response(serialized_data_with_count, status=status.HTTP_200_OK)
    
class AllCategoriesView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'msg': 'An error occurred'}, status=500)