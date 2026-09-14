"""Render the site to static HTML so it can be served without a running server."""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import RequestFactory
from django.urls import resolve

from mysite.content import PROJECTS_DIR, load_projects

# Pages that always exist, mapped to their file in the build output.
STATIC_PAGES = {
    "/": "index.html",
    "/resume/": "resume/index.html",
}

# The projects section is held back for now, so nothing under /projects/ is
# built. To publish it, set this to True and restore the Projects link in
# layout.html.
PUBLISH_PROJECTS = False


class Command(BaseCommand):
    help = "Render the site to static HTML in the output directory."

    def add_arguments(self, parser):
        parser.add_argument("--output", default="out")

    def handle(self, *args, **options):
        out = Path(options["output"]).resolve()
        if out.exists():
            shutil.rmtree(out)

        call_command("collectstatic", interactive=False, clear=True, verbosity=0)
        shutil.copytree(settings.STATIC_ROOT, out / "static")

        projects = load_projects() if PUBLISH_PROJECTS else []
        pages = dict(STATIC_PAGES)
        if PUBLISH_PROJECTS:
            pages["/projects/"] = "projects/index.html"
        for project in projects:
            pages[f"/projects/{project.slug}/"] = f"projects/{project.slug}/index.html"

        factory = RequestFactory()
        for url, target in pages.items():
            match = resolve(url)
            response = match.func(factory.get(url), *match.args, **match.kwargs)
            if hasattr(response, "render"):
                response.render()

            # Fail the build rather than publishing an error page.
            if response.status_code != 200:
                raise CommandError(f"{url} returned {response.status_code}")

            destination = out / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(response.content)
            self.stdout.write(f"{url} -> {target}")

        # Copy each published project's images next to its page, so relative
        # image paths in a writeup resolve the same way they do locally.
        for project in projects:
            shutil.copytree(
                PROJECTS_DIR / project.slug,
                out / "projects" / project.slug,
                ignore=shutil.ignore_patterns("*.md"),
                dirs_exist_ok=True,
            )
