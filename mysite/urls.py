from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from . import views
from .content import PROJECTS_DIR

urlpatterns = [
    path("", views.index, name="index"),
    path("resume/", views.resume, name="resume"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project, name="project"),
]

if settings.DEBUG:
    # Project images live next to their writeups. render_static copies them into
    # the build; this serves them the same way under runserver.
    urlpatterns += [
        re_path(r"^projects/(?P<path>[\w-]+/.+\.\w+)$", serve, {"document_root": PROJECTS_DIR}),
    ]
