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
Resume entries live in `resume.json` at the top level, newest first. Edit the file,
commit, and push. Vercel rebuilds on every push to `main`.

Each role has:

- `title`, `company`
- `short_title`: a shorter title for the chart label (optional; defaults to `title`)
- `start`, `end`: months as `"YYYY-MM"`. Use `null` for `end` on your current role.
- `summary`, `details`: the role's full write-up, shown when the role is selected
  in the chart. Long write-ups fade out with "See more", and expanded ones end
  with "Collapse". Leave `details` empty for none.

The chart's timeline, bar sizes, and tenure are all worked out from the dates.

# Adding a project
The projects section is built but not published yet: `PUBLISH_PROJECTS` in
`render_static.py` is off and the Projects link is out of the nav. Pages still
work locally under `runserver`. To publish, turn the flag on and restore the link
in `layout.html`.

Each project is a folder in `content/projects/`. The folder name becomes the URL
(`content/projects/rested/` is served at `/projects/rested/`).

Inside the folder, `index.md` holds the writeup, with settings at the top:

```
---
title: Rested
summary: One sentence, shown on the card and under the title.
date: 2026
tags: iOS, HealthKit
cover: cover.jpg
website: https://...
app_store: https://...
github: https://...
order: 2
draft: true
---

The writeup, in Markdown.
```

Only `title` and `summary` are required. Put images in the same folder and reference
them by filename (`![Wiring](wiring.jpg)`). `cover` is used for the card and the page
header, and the build fails if the file isn't there. Lower `order` comes first, and
the first project gets the large featured card.

`draft: true` hides a project from the live site but shows it locally and on Vercel
preview deployments, so you can review it on a branch before publishing.

# What's Included
1. **resume.json**: resume content, the source of truth for the `/resume/` page.
2. **content/projects/**: one folder per project page, with its writeup and images.
3. **requirements.txt**: the three packages needed to render the site.
4. **config/settings.py**: Django settings, trimmed to what a static render needs.
5. **mysite folder**:
   1. **views.py**: view functions for the site (index, resume).
   2. **static folder**: visuals and CSS used across the site.
   3. **templates folder**: HTML templates for each page.
   4. **content.py**: loads the resume and project content.
   5. **management/commands/render_static.py**: the static site renderer.

# Deployment
Hosted on Vercel. Pushes to `main` trigger a build that runs `render_static` and
publishes `out/`. Build settings live in `vercel.json`.

To add a new kind of page, add its URL to `STATIC_PAGES` in `render_static.py`.
Project pages are picked up automatically.
