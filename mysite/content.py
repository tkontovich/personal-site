"""Load the site's content: resume entries and project writeups."""

import json
import math
import os
from dataclasses import dataclass, field
from datetime import date
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


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _parse_month(value):
    year, month = value.split("-")
    return int(year), int(month)


def _month_number(year_month):
    year, month = year_month
    return year * 12 + month - 1


def _format_month(year_month):
    year, month = year_month
    return f"{MONTH_NAMES[month - 1]} {year}"


def _percent(value):
    return f"{value:.3f}%"


def format_tenure(months):
    """Return (value, unit) for a length of time, like ("5.3", "years").

    resume.html has a JavaScript copy of this that keeps the current role's
    tenure up to date between deploys, so the two must round the same way.
    """
    if months < 12:
        return str(months), "month" if months == 1 else "months"
    years = math.floor(months / 12 * 10 + 0.5) / 10
    return f"{years:.1f}".removesuffix(".0"), "years"


def load_resume(today=None):
    """Load resume.json and lay the roles out on one shared timeline.

    `start` and `end` are "YYYY-MM"; a role without an `end` is current and runs
    to today. The chart covers whole years, from January of the earliest start
    to the January after the latest end.
    """
    today = today or date.today()
    this_month = (today.year, today.month)
    jobs = json.loads(RESUME_PATH.read_text(encoding="utf-8"))

    for index, job in enumerate(jobs):
        start = _parse_month(job["start"])
        end = _parse_month(job["end"]) if job.get("end") else None
        job["key"] = f"role-{index}"
        job["is_current"] = end is None
        job["start_month"] = start
        job["end_month"] = end or this_month
        job["dates"] = f"{_format_month(start)} \u2013 {_format_month(end) if end else 'Present'}"
        job["months"] = _month_number(job["end_month"]) - _month_number(start)
        job["tenure_value"], job["tenure_unit"] = format_tenure(job["months"])
        job["short_title"] = job.get("short_title") or job["title"]
        job["tags"] = job.get("tags") or []
        # Numbers like "408%" get the large display size; phrases get a smaller one.
        job["figure_is_phrase"] = any(char.isalpha() for char in job.get("figure", ""))

    first_year = min(job["start_month"][0] for job in jobs)
    last_year = max(job["end_month"][0] for job in jobs) + 1
    domain_start = first_year * 12
    domain_months = (last_year - first_year) * 12

    for job in jobs:
        offset = _month_number(job["start_month"]) - domain_start
        job["left"] = _percent(offset / domain_months * 100)
        job["width"] = _percent(job["months"] / domain_months * 100)
        if job["months"] >= 24:
            ends = "now" if job["is_current"] else job["end_month"][0]
            job["bar_label"] = f"{job['start_month'][0]}\u2013{ends}"
        else:
            job["bar_label"] = ""

    selected = next((job for job in jobs if job["is_current"]), jobs[0])
    for job in jobs:
        job["is_selected"] = job is selected

    return {
        "jobs": jobs,
        "timeline": sorted(jobs, key=lambda job: _month_number(job["start_month"])),
        "ticks": [
            {"year": year, "left": _percent((year - first_year) * 12 / domain_months * 100)}
            for year in range(first_year, last_year + 1)
        ],
        "domain_start": f"{first_year}-01",
        "domain_months": domain_months,
    }


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
