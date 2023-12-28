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

base_url = settings.BASE_URL
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class StripeCheckoutView(APIView):
    def post(self, request, courseId, user):
        try:
            
            user_instance = User.objects.get(username=user)
            course = Course.objects.get(id=courseId)  
            coursePrice = course.price
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
                success_url=settings.SITE_URL + '/mylearnings/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            
            payment = Payment.objects.create(
                course=course,
                user=user_instance,
                chef=course.instructor,
                amount=coursePrice,
                status='success',
                payed=True,
                payment_date=timezone.now(),
            )
            payment.save()
            
            return redirect(checkout_session.url)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
