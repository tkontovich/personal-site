import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render


RESUME_PATH = Path(settings.BASE_DIR) / "resume.json"


def index(request):
    return render(request, "mysite/index.html")


def resume(request):
    jobs = json.loads(RESUME_PATH.read_text(encoding="utf-8"))

    return render(request, "mysite/resume.html", {
        "jobs": jobs
    })
