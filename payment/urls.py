from django.urls import path
from .views import *

urlpatterns = [
    path('create-checkout-session/<int:courseId>/<str:user>/', StripeCheckoutView.as_view()),
    path('success-checkout/',SuccessCheckOut.as_view(),name='success_checkout'),
]
