"""
URL configuration for personal site project.
"""
from django.urls import include, path

urlpatterns = [
    path("", include("mysite.urls"))
]
