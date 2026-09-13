"""Load the site's content: resume entries and project writeups."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

import markdown2
from django.conf import settings

RESUME_PATH = Path(settings.BASE_DIR) / "resume.json"
PROJECTS_DIR = Path(settings.BASE_DIR) / "content" / "projects"

# Drafts show everywhere except the production deployment, so they can be
# reviewed locally and on Vercel preview deployments before going live.
SHOW_DRAFTS = os.getenv("VERCEL_ENV") != "production"

# Front matter keys that become link buttons, in display order.
LINK_LABELS = {
    "website": "Visit site",
    "app_store": "App Store",
    "github": "GitHub",
}

MARKDOWN_EXTRAS = ["metadata", "fenced-code-blocks", "tables", "markdown-in-html"]


def load_resume():
    return json.loads(RESUME_PATH.read_text(encoding="utf-8"))


@dataclass
class Project:
    slug: str
    title: str
    summary: str
    body_html: str
    date: str = ""
    tags: list = field(default_factory=list)
    cover: str = ""
    links: list = field(default_factory=list)
    order: int = 100
    draft: bool = False

    @property
    def cover_url(self):
        return f"/projects/{self.slug}/{self.cover}" if self.cover else ""


def _load_project(path):
    html = markdown2.markdown(path.read_text(encoding="utf-8"), extras=MARKDOWN_EXTRAS)
    meta = {key: str(value).strip() for key, value in html.metadata.items()}
    slug = path.parent.name

    cover = meta.get("cover", "")
    if cover and not (path.parent / cover).is_file():
        raise ValueError(f"{path}: cover image '{cover}' not found next to index.md")

    return Project(
        slug=slug,
        title=meta.get("title", slug),
        summary=meta.get("summary", ""),
        body_html=str(html),
        date=meta.get("date", ""),
        tags=[tag.strip() for tag in meta.get("tags", "").split(",") if tag.strip()],
        cover=cover,
        links=[
            {"label": label, "url": meta[key]}
            for key, label in LINK_LABELS.items()
            if meta.get(key)
        ],
        order=int(meta.get("order", 100)),
        draft=meta.get("draft", "").lower() == "true",
    )


def load_projects():
    projects = (_load_project(path) for path in PROJECTS_DIR.glob("*/index.md"))
    visible = [project for project in projects if SHOW_DRAFTS or not project.draft]
    return sorted(visible, key=lambda project: (project.order, project.title))
