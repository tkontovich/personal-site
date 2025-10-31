from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .models import Job

import json


### Set up global variables 
# from .models import modelsgohere


# Create your views here.

def index(request):
    return render(request, "mysite/index.html")
    

 


def login(request):
    return render(request, "mysite/login.html")


def logout(request):
    return render(request, "mysite/index.html")


def resume(request):
    jobs = Job.objects.all()

    return render(request, "mysite/resume.html", {
        "jobs": jobs
    })
