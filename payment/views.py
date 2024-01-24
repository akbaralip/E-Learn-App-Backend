from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.conf import settings
from .models import Payment
from users.models import User
from course.models import Course
from django.utils import timezone
from django.shortcuts import redirect
import stripe
from rest_framework import status

base_url = settings.BASE_URL
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class StripeCheckoutView(APIView):
    def post(self, request, courseId, user):
        try:
            
            user_instance = User.objects.get(username=user)
            course = Course.objects.get(id=courseId)  
            coursePrice = course.price
            course_instructor = course.instructor
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': course.title,
                                'images':['https://images.pexels.com/photos/3769739/pexels-photo-3769739.jpeg']     
                            },
                            'unit_amount': int(coursePrice * 100), 
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                # success_url=settings.SITE_URL + '/mylearnings/?success=true&session_id={CHECKOUT_SESSION_ID}',

                success_url=f'https://akbarali.shop/success-checkout/?success=true&session_id={{CHECKOUT_SESSION_ID}}&course={course}&coursePrice={coursePrice}&user_instance={user_instance}&course_instructor={course_instructor}',

                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            
            # payment = Payment.objects.create(
            #     course=course,
            #     user=user_instance,
            #     chef=course.instructor,
            #     amount=coursePrice,
            #     status='success',
            #     payed=True,
            #     payment_date=timezone.now(),
            # )
            # payment.save()
            
            return redirect(checkout_session.url)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class SuccessCheckOut(APIView):
    def get(self, request):
        try:
            course = request.query_params.get('course')  
            coursePrice = request.query_params.get('coursePrice')
            user_instance = request.query_params.get('user_instance')
            course_instructor = request.query_params.get('course_instructor')

            print(f'course: {course}')
            print(f'user_price: {coursePrice}')
            print(f'user_instance: {user_instance}')
            print(f'course_instructor: {course_instructor}')

            payment = Payment.objects.create(
                course=course,
                user=user_instance,
                chef=course_instructor,
                amount=coursePrice,
                status='success',
                payed=True,
                payment_date=timezone.now(),
            )
            payment.save()
            success_url=settings.SITE_URL + '/mylearnings/?success=true&session_id={CHECKOUT_SESSION_ID}'
            return redirect(success_url)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)