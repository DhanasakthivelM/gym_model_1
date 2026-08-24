# IRONVEIN — High-End Gym Website

A premium, single-package gym website: **Python (Flask) backend + HTML/CSS/JS frontend**,
themed in **red, black & gold**, with a floating **WhatsApp** button and heavy scroll/hover
animations.

## Features
- Animated hero with parallax glow, ambient background zoom, and line-by-line title reveal
- Sticky glass navbar + mobile hamburger menu
- Scroll-triggered reveal animations throughout (About, Features, Packages, Testimonials, Contact)
- Animated counters (years, members, coaches, retention)
- 3 gym membership **packages** rendered from Python data (easy to edit/add more)
- **Features/amenities** grid with hover shine effect
- Dedicated **video section** to showcase a gym walkthrough (drop your MP4 in, see below)
- Testimonials, working **contact form** (POST → saved to `messages.json`), footer
- Floating **WhatsApp button** (pulsing, tooltip, deep-links straight into a chat)
- Fully responsive: desktop, tablet, mobile
- Custom cursor + magnetic hover states on desktop

## 1. Install
```bash
pip install -r requirements.txt
```

## 2. Run
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

## 3. Customize
Almost everything is controlled from the top of **`app.py`**:

| What to change            | Where                          |
|----------------------------|---------------------------------|
| Gym name, tagline, address | `SITE` dictionary               |
| WhatsApp number             | `SITE["whatsapp_number"]` (country code + number, no `+` or spaces) |
| Opening hours               | `SITE["hours"]`                 |
| Membership packages/prices  | `PACKAGES` list                 |
| Features / amenities        | `FEATURES` list                 |
| Testimonials                | `TESTIMONIALS` list              |
| Stats (years, members, etc) | `STATS` list                    |

Colors, fonts and animation timing live in `static/css/style.css` under the
`:root { ... }` variables at the top of the file — change `--red`, `--gold`, `--black`
to re-theme the whole site instantly.

## 4. Add your gym's video
Drop an MP4 file here:
```
static/videos/gym-tour.mp4
```
The "Inside The Gym" section will automatically play it — no code changes needed.
(You can also swap the poster/thumbnail image in `templates/index.html`, search for `video-wrap`.)

## 5. Contact form submissions
Form submissions are saved locally to `messages.json` (auto-created) so you have a simple
log of every lead — no database required. Swap `save_message()` in `app.py` for an email/DB
integration whenever you're ready.

## Folder structure
```
gym-website/
├── app.py                  # Flask backend + all site content/config
├── requirements.txt
├── messages.json           # created automatically on first form submit
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    ├── js/script.js
    ├── videos/gym-tour.mp4  # ← add your video here
    └── images/
```

## Deploying
This is a standard Flask app — deploy it anywhere Python apps run (Render, Railway,
PythonAnywhere, a VPS with gunicorn + nginx, etc). For production, run with gunicorn instead
of the built-in dev server:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
and remember to change `app.secret_key` in `app.py` to a real secret.
