from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancy.urls')),
    path('', include('resume.urls')),
]
