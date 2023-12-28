
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('', include('adminside.urls')),
    path('', include('profile_app.urls')),
    path('', include('course.urls')),
    path('api/stripe/', include('payment.urls')),
    path('',include('chat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)