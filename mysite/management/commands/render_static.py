"""Render the site to static HTML so it can be served without a running server."""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import RequestFactory
from django.urls import resolve

# Every page on the site, mapped to its file in the build output.
PAGES = {
    "/": "index.html",
    "/resume/": "resume/index.html",
}


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

        factory = RequestFactory()
        for url, target in PAGES.items():
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
