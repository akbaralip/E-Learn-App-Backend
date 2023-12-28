from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class Profile(APIView):
    def get(self, request):
        try:
            username = request.query_params.get('username')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        upload_file = request.FILES.get('file')
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if upload_file:
            user.image = upload_file
            user.save()
            image_url = user.image.url
            return Response({'message': 'File uploaded successfully', 'user_image': image_url}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    def put(self, request, profile_id, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        contact = request.data.get('phone')

        try:
            user = User.objects.get(id=profile_id)
            if User.objects.filter(username=username).exclude(id=profile_id).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.username = username
            user.phone = contact
            user.email = email
            user.save()

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
from django.contrib.auth.hashers import check_password
class ChangePassword(APIView):
    def put(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
            
            current_password = request.data.get('password', '')
            new_password = request.data.get('new_password', '')
            

            if check_password(current_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'})
            else:
                return Response({'status': 'error', 'message': 'Current password is incorrect'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=500)