# AI-Based Adaptive Study Dashboard

This project is a small demo of an **adaptive user interface** (AUI) using
simple AI-style logic (a lightweight user model) to adapt the UI based on
user interaction patterns.

## Overview

The page shows several "modules" (cards). Each card has:

- A short summary (always visible)
- A hidden "details" section
- A button to toggle details ("Show more details" / "Hide details")

As you interact:

- Every time you expand details, the system counts it as a preference
  for **more** information.
- Every time you hide details, it counts as a preference for **less**
  information.

When you click **"Adapt interface (AI)"**, a simple rule infers your
profile:

- If you usually expand details, the UI switches to **Expert** mode
  (smaller fonts, denser layout).
- Otherwise, it switches to **Beginner** mode (larger fonts, more
  spacing, simpler appearance).

## Tech stack

- HTML
- CSS
- JavaScript (no build step, no backend)

To run:

1. Open `index.html` in any modern browser.
2. Click "Show more details"/"Hide details" a few times.
3. Click **"Adapt interface (AI)"** to update the layout based on your
   behavior.

You can extend this with:

- More sophisticated machine learning models
- Server-side logging
- User accounts and persistent profiles
