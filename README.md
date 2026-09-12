# Description
Welcome to my personal website project! This is a Django site that contains info about me and my resume.

Django is used as a **build-time tool only**. `manage.py render_static` renders the
templates to plain HTML in `out/`, and that directory is what gets served. There is
no application server, no database, and nothing running between deploys.

# How to Run
1. Navigate to the top level directory
2. Create a virtual environment and install `requirements.txt`
3. Use `python3 manage.py runserver` to preview the site locally
4. Use `python3 manage.py render_static` to produce the deployable `out/` directory

# Editing the resume
Resume entries live in `resume.json` at the top level. Each entry has a `title`,
`company`, `dates`, and a `description` written in Markdown. Edit the file, commit,
and push — Vercel rebuilds on every push to `main`.

Order in the file is the order on the page.

# What's Included
1. **resume.json**: resume content, the source of truth for the `/resume/` page.
2. **requirements.txt**: the three packages needed to render the site.
3. **config/settings.py**: Django settings, trimmed to what a static render needs.
4. **mysite folder**:
   1. **views.py**: view functions for the site (index, resume).
   2. **static folder**: visuals and CSS used across the site.
   3. **templates folder**: HTML templates for each page.
   4. **management/commands/render_static.py**: the static site renderer.

# Deployment
Hosted on Vercel. Pushes to `main` trigger a build that runs `render_static` and
publishes `out/`. Build settings live in `vercel.json`.

To add a page, add its URL to `PAGES` in `render_static.py` so the renderer picks it up.
