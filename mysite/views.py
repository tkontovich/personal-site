from django.http import Http404
from django.shortcuts import render

from .content import load_projects, load_resume


def index(request):
    return render(request, "mysite/index.html")


def resume(request):
    return render(request, "mysite/resume.html", {
        "resume": load_resume()
    })


def projects(request):
    return render(request, "mysite/projects.html", {
        "projects": load_projects()
    })


def project(request, slug):
    for candidate in load_projects():
        if candidate.slug == slug:
            return render(request, "mysite/project.html", {
                "project": candidate
            })
    raise Http404(f"No project named {slug}")
