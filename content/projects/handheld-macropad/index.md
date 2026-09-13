---
title: Handheld Macropad
summary: A handheld macro keypad I built and flashed with custom ZMK firmware.
date: 2026
tags: Electronics, Firmware, ZMK
github: https://github.com/tkontovich/handheld-macro-keypad
order: 1
draft: true
---

*Draft: this is placeholder copy. Replace it with your own writeup and add photos, then remove `draft: true` above to publish.*

## What it is

*A sentence or two on what the macropad does and why you wanted one.*

## How it's built

The keypad runs [ZMK](https://zmk.dev), an open-source keyboard firmware built on Zephyr. It's defined as a custom shield: an overlay describes how the keys are wired to the controller, a keymap sets what each key does, and a GitHub Actions workflow builds the firmware image ready to flash.

*Add: the controller board, switches, case, and how you put it together.*

## What I learned

*What was harder than expected, and what you'd do differently next time.*

<!--
Adding photos: put image files in this folder, next to index.md.

A single full-width photo:

![The finished macropad](finished.jpg)

A grid of photos. Leave a blank line between each image:

<div class="gallery" markdown="1">

![Wiring](wiring.jpg)

![Case](case.jpg)

</div>

To use one as the card and header image, add `cover: finished.jpg` to the front matter.
-->
