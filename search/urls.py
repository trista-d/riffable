"""
Django url mapping. Add paths for new views below. 
Create functions in views.py corresponding with path names.

For more info: https://docs.djangoproject.com/en/3.1/ref/urls/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # '' tells Django this is the site's homepage (no extra path at the end of url)
    path('play.html', views.play, name="play")
]