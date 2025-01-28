from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('create_job_post')),  # Redirect root URL to create_job
    path('', include('my_app.urls')),  # Include your app's URL patterns only here
]
