from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("resume/", views.resume, name="resume"),
    path("goals/", cache_page(60 * 120)(views.goals2024), name="goals2024"),

    #API ROUTES
    path("contact/", views.contact, name="contact")

]

