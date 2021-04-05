"""
Django url mapping. 
This is not the same as search/urls.py

https://docs.djangoproject.com/en/3.1/ref/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')), # 'search' is the folder containing views.py and the other urls.py
]