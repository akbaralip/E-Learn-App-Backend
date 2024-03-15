from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes , force_str
from .token import generate_token
from django.conf import settings
from rest_framework import status

from .serializers import *


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import random
from django.core.mail import send_mail, EmailMessage
import string

from .models import User
from payment.models import Payment
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_active'] = user.is_active

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            username = request.data['username']
            
            try:
                user = User.objects.get(username=username)
                
                if user.image:
                    image_url = user.image.url
                else:
                    image_url = None


                if user.is_superuser:
                    role = 'admin'
                elif user.is_chef:
                    role = 'chef'
                else:
                    role = 'user'

                response.data['username'] = username
                response.data['user_id'] = user.pk
                response.data['role'] = role
                response.data['image_url'] = image_url



            except User.DoesNotExist:
                response.data['error'] = 'User not found'
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        return response
    
      




def generate_otp(length=4):
    characters = string.digits  
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


from django.core.mail import send_mail

class RegisterView(APIView):
    def post(self, request):
        existing_username = User.objects.filter(username=request.data.get('username')).first()
        if existing_username:
            return Response({'message': 'Username already exists. Please choose another one.'}, status=400)
        
        
        # existing_email = User.objects.filter(email=request.data.get('email')).first()
        # if existing_email:
        #     return Response({'message': f'Email already exists.Please use a different email address.'}, status=400)
        
        serializer = UserSerializer(data=request.data)
      
        if serializer.is_valid():
            otp = generate_otp()
            print('===========================>', otp)
            
            validated_data = serializer.validated_data
            password = validated_data.pop('password', None)
            
            user = serializer.save()
            
            user.set_password(password)
            
            user.otp = otp
            user.save()
           
            subject = 'OTP for Registration'
            message = f'Hello dear {user}, Your OTP for registration is: {otp}'
            from_email = 'akbaralip7777@gmail.com' 
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response(serializer.data)
        else:
            return Response({'message': 'Error during registration.', 'errors': serializer.errors}, status=400)


class OtpVerificationView(APIView):
    def post(self, request):
        user_otp = request.data.get('otp')
        if not user_otp:
            return Response({'message': 'OTP is missing'}, status=400)
        
        try:
            user = User.objects.get(otp=user_otp)
        except User.DoesNotExist:
            return Response({'message': 'Invalid OTP'}, status=400)
        
        if not user.is_active:
            user.is_active = True  
            user.save()
            user.otp = ""
            
            user_data = {
                'username': user.username,
                'email': user.email,
            }
        
            return Response({'message': 'OTP verified successfully', 'user_data': user_data})
        else:
            return Response({'message': 'User is already active'}, status=400)


class ForgetPasswordView(APIView):
     def post(self,request):
            try:
                email = request.data.get('email')   
                myuser=User.objects.filter(email=email).first()
                
                current_site = get_current_site(request)
                email_subject = 'confirm Your email @ Chef-Charisma'
                message2 = render_to_string('forgot_password_mail.html',{
                        'name': myuser.username ,   
                        'domain': current_site.domain ,
                        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                        'token': generate_token.make_token(myuser),
                })
                email = EmailMessage(
                        email_subject,message2,
                        settings.EMAIL_HOST_USER,
                        [myuser.email] 
                )

                email.fail_silently = True
                email.send()

                return Response({'message': 'email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def forgot_password_mail_view(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        
        session = settings.SITE_URL + '/change_password/?uidb64=' + uidb64
        
        return HttpResponseRedirect(session)   


class ResetPassword(APIView):
    def post(self,request):
        password = request.data.get('password')
        uidb64 = request.data.get('uidb64')
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            myuser=User.objects.get(pk=uid)
        except(TypeError,ValueError,OverflowError, User.DoesNotExist):
            myuser=None
        if myuser is not None:
            myuser.set_password(password)
            myuser.save()
            return JsonResponse({'message': 'Password reset successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid or expired reset link'}, status=400)

class ChefListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            chefs = User.objects.filter(is_chef=True).order_by('id')[:4]
            chef_list = []

            for chef in chefs:
                chef_list.append({
                    'id': chef.id,
                    'name': chef.username,
                    'image_url': chef.image.url if chef.image else None,
                })

            return Response({'chefs': chef_list})
        except Exception as e:
            return Response({'error': str(e)})
        

class ChefStudentsList(APIView):
    def get(self, request, user_id):
        serializer = UserSerializer
        chef = User.objects.get(id=user_id, is_chef=True)
        chef_payments = Payment.objects.filter(chef=chef, status='success', payed=True)
        unique_users = set(payment.user for payment in chef_payments)
        serialized_data = serializer(unique_users, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    

class AdminDetailsView(APIView):
    def get(self, request):
        try:
            admin_user = User.objects.get(is_admin=True)
            admin_details = {
                'admin_user_id': admin_user.id,
                'admin_username': admin_user.username,
            }
            return Response(admin_details, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Admin user not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllChefsAPIView(APIView):
    def get(self, request, format=None):
        chefs = User.objects.filter(is_chef=True)
        serializer = ChefSerializer(chefs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
