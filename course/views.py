from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Category
from .serializers import *
from users.models import User  
from .models import CourseVideos
from payment.models import Payment


class UploadCourse(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            instructor = request.data.get('instructor')
            category = request.data.get('category')
            video = request.data.get('video')
            price = request.data.get('price')
            cover_image = request.data.get('coverImage')
            about = request.data.get('about')

            user = User.objects.get(id=instructor)
            category_obg = Category.objects.get(id=category)

            Course.objects.create(
                title=title,
                description=description,
                category=category_obg,
                instructor=user,
                demo_video=video,
                price=price,
                cover_image=cover_image,
                about=about,

            )
            
            return Response({'success': 'Course created successfully'}, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({'error': 'One or more fields contain values that are too long.'}, status=status.HTTP_400_BAD_REQUEST)

class UploadCourseVideo(APIView):
    def post(self, request, course_id):
        try:
            course= Course.objects.get(id=course_id)
            title = request.data.get('title')
            description = request.data.get('description')
            video = request.FILES.get('video')


            if video is not None:
                a = CourseVideos.objects.create(
                    course=course,
                    title=title,
                    description=description,
                    videos=video,
                    )
                a.save()
                print(a)
            else:
                return Response({'error': 'Video file is required'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'Course based video created successfully'}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

class MarkCourseListed(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            course.is_listed = True
            course.save()
            return Response({'message': 'Course listed successfully'})
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'})


class CourseView(APIView):
    def get(self, request):
        courses = Course.objects.filter(is_listed=True)
        categories = Category.objects.values('id', 'category')
        price_values = Course.objects.values('price').distinct()

        serializer = CourseSerializer(courses, many=True)
        
        return Response({
            'courses': serializer.data,
            'categories': categories,
            'prices': price_values,
        }, status=status.HTTP_200_OK)
    
class ChefCourseView(APIView):
    def get(self, request, user_id):
        courses = Course.objects.filter(instructor=user_id)
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'courses': serializer.data,
        }, status=status.HTTP_200_OK)

class ChefUnListCourseView(APIView):
    def get(self, request, user_id):
        courses = Course.objects.filter(instructor=user_id, is_listed=False)
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'courses': serializer.data,
        }, status=status.HTTP_200_OK)

class ChefListedCourseView(APIView):
    def get(self, request, user_id):
        courses = Course.objects.filter(instructor=user_id, is_listed=True)
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'courses': serializer.data,
        }, status=status.HTTP_200_OK)

class CourseListByCategory(APIView):
    def get(self, request, category):
        try:
            courses = Course.objects.filter(category_id=category, is_listed=True)
            serialized_courses = CourseSerializer(courses, many=True).data
            return Response(serialized_courses, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseListByChefs(APIView):
    def get(self, request, chefId):
        try:
            courses = Course.objects.filter(instructor=chefId, is_listed=True)
            serialized_courses = CourseSerializer(courses, many=True).data
            return Response(serialized_courses, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CoursesVideosView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.filter(id=course_id)
            videos = CourseVideos.objects.filter(course=course_id)
            courses = CourseSerializer(course,many=True)
            serializer = VideoSerializer(videos, many=True)
            return Response({'videos': serializer.data , 'course':courses.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EditCourse(APIView):
    def put(self, request, video_id):
        try:
            chapter = CourseVideos.objects.get(id=video_id)
        except CourseVideos.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
        title = request.data.get('title')
        description = request.data.get('description')
        new_video = request.FILES.get('video')

        if new_video:
            chapter.videos = new_video
        if description:
            chapter.description = description
        if title:
            chapter.title = title
        chapter.save()
            
        return Response({"message": 'success'})


class DeleteCourseVideo(APIView):
    def delete(self, request, video_id):
        try:
            chapter = CourseVideos.objects.get(id=video_id)
            print('its a delete view')
        except CourseVideos.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        chapter.delete()
        return Response({"message": "Video deleted successfully"})

class DeleteCourse(APIView):
    def delete(self, request, course_id):
        try:
            course = Course.objects.filter(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response({"message": "Course deleted successfully"})
            
        

        

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response( {'categories': serializer.data}, status=status.HTTP_200_OK)
    

class InstructorsList(APIView):
    def get(self, request, instructor_id):
        try:
            instructor = User.objects.filter(id=instructor_id).first()
            instructor_data = []

            if instructor:
                instructor_data.append({
                    'id': instructor.id,
                    'username': instructor.username,
                    'email': instructor.email,
                    'profile_image_url': instructor.image.url if instructor.image else '',
                })

            return Response({'instructors': instructor_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckCoursePurchaseStatus(APIView):
    def get(self, request, courseId, user):
        try:
            user_instance = User.objects.get(username=user)
            course_instance = Course.objects.get(id=courseId)

            is_purchased = Payment.objects.filter(
                user=user_instance,
                course=course_instance,
                status='success'
            ).exists()

            return Response({'isPurchased': is_purchased})
        except (User.DoesNotExist, Course.DoesNotExist) as e:
            return Response({'error': str(e)}, status=404)
        
class PurchasedCourses(APIView):
    def get(self, request, user_id):
        
        purchsed_user = Payment.objects.filter(user=user_id)
        purchased_courses = [payment.course for payment in purchsed_user]
        serializer = PaymentSerializer(purchsed_user, many=True)

        if not purchsed_user.exists():
            return Response({'message': 'User has no successful payments.'})
        return Response({'purchased': serializer.data})
        
class PurchasedCoursesVideos(APIView):
    def get(self, request, course_id):
        course_videos = CourseVideos.objects.filter(course=course_id)
        serializer = ChapterSerializer(course_videos, many=True)
        
        return Response(serializer.data)
    
class CheckUserPurchased(APIView):
    def get(self, request, user_name):
        try:
            user = User.objects.get(username=user_name)
            purchases = Payment.objects.filter(user=user, payed=True)  
            if purchases.exists():
                return Response({'message': 'True'})
            else:
                return Response({'message': 'False'})
        except User.DoesNotExist:
            return Response({'message': 'User not found'})
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'})


class ChefEarningsView(APIView):
    def get(self, request, user_id):
        chef_earnings = Payment.objects.filter(chef=user_id)
        serializer = ChefEarningsSerializer(chef_earnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddCategory(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Successfully added a new category'})
        else:
            errors = serializer.errors
            print('Validation errors:', errors)
            return Response({'error': 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategory(APIView):
    def delete(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return Response({'msg':'Category deleted successfully'})
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        