
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Hostel APIs
    path('api/', include('hostel.urls')),

    # Login API
    path('api/login/', obtain_auth_token, name='api_login'),
]
