"""
IRONVEIN GYM — Flask backend
A single-package static-style website (Python backend + HTML/CSS/JS frontend).

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "ironvein-secret-key-change-in-production"

# --------------------------------------------------------------------------
# SITE CONFIG — edit this block to re-brand the whole site
# --------------------------------------------------------------------------
SITE = {
    "name": "IRONVEIN",
    "tagline": "FORGE YOUR LEGEND",
    "subtitle": "A private strength temple where black steel meets gold discipline.",
    "phone_display": "+91 98765 43210",
    "whatsapp_number": "919876543210",   # country code + number, no + or spaces
    "email": "hello@ironveingym.com",
    "address": "12 Anna Salai, RS Puram, Coimbatore, Tamil Nadu 641002",
    "hours": [
        {"days": "Monday – Friday", "time": "5:00 AM – 11:00 PM"},
        {"days": "Saturday",        "time": "6:00 AM – 10:00 PM"},
        {"days": "Sunday",          "time": "7:00 AM – 9:00 PM"},
    ],
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
}

WHATSAPP_DEFAULT_MESSAGE = "Hi IRONVEIN, I'd like to know more about your membership plans."

# --------------------------------------------------------------------------
# GYM PACKAGES
# --------------------------------------------------------------------------
PACKAGES = [
    {
        "id": "bronze",
        "name": "Ignite",
        "tier": "Starter",
        "price": 1999,
        "period": "month",
        "featured": False,
        "perks": [
            "Full gym floor access",
            "Locker & shower access",
            "1 free fitness assessment",
            "Access to mobile app tracker",
            "Standard hours (5 AM – 9 PM)",
        ],
    },
    {
        "id": "gold",
        "name": "Ascend",
        "tier": "Most Popular",
        "price": 3999,
        "period": "month",
        "featured": True,
        "perks": [
            "Everything in Ignite",
            "24/7 gym floor access",
            "4 personal training sessions / month",
            "Nutrition & macro planning",
            "Sauna, steam & recovery zone",
            "Guest passes ×2 / month",
        ],
    },
    {
        "id": "platinum",
        "name": "Sovereign",
        "tier": "Elite",
        "price": 7999,
        "period": "month",
        "featured": False,
        "perks": [
            "Everything in Ascend",
            "Unlimited personal training",
            "Private locker + towel service",
            "Monthly body-composition scan",
            "Priority class booking",
            "Dedicated concierge coach",
        ],
    },
]

# --------------------------------------------------------------------------
# FEATURES / AMENITIES
# --------------------------------------------------------------------------
FEATURES = [
    {"icon": "dumbbell", "title": "Elite Strength Floor",
     "desc": "Premium free-weight rigs, competition platforms and a full range of resistance machines."},
    {"icon": "heartbeat", "title": "Performance Cardio Deck",
     "desc": "Skyline-facing treadmills, rowers and assault bikes with live heart-rate tracking."},
    {"icon": "user-friends", "title": "Certified Coaches",
     "desc": "One-on-one programming from coaches trained in strength, physique and rehab work."},
    {"icon": "utensils", "title": "Nutrition Studio",
     "desc": "Custom macro plans and an in-house protein bar to fuel every session."},
    {"icon": "spa", "title": "Recovery & Sauna",
     "desc": "Infrared sauna, cold plunge and guided mobility rooms to rebuild between lifts."},
    {"icon": "shield-alt", "title": "24/7 Secure Access", "desc": "Biometric entry, HD security and round-the-clock staffed hours for peace of mind."},
]

TESTIMONIALS = [
    {"name": "Arjun Mehta", "role": "Member since 2023",
     "quote": "IRONVEIN rebuilt my discipline. The coaching is elite and the space feels like nowhere else in the city."},
    {"name": "Sneha Kapoor", "role": "Ascend member",
     "quote": "Best decision I made this year. The recovery zone alone is worth the membership."},
    {"name": "Rahul Varma", "role": "Sovereign member",
     "quote": "Private coaching, real results. I've never trained anywhere this serious about performance."},
]

STATS = [
    {"value": 12, "suffix": "+", "label": "Years Forging Athletes"},
    {"value": 3200, "suffix": "+", "label": "Active Members"},
    {"value": 40, "suffix": "+", "label": "Expert Coaches"},
    {"value": 98, "suffix": "%", "label": "Member Retention"},
]

MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "messages.json")


def save_message(entry: dict) -> None:
    """Append a contact-form submission to a local JSON log."""
    data = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []
    data.append(entry)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def home():
    return render_template(
        "index.html",
        site=SITE,
        packages=PACKAGES,
        features=FEATURES,
        testimonials=TESTIMONIALS,
        stats=STATS,
        whatsapp_msg=WHATSAPP_DEFAULT_MESSAGE,
        year=datetime.now().year,
    )


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    goal = request.form.get("goal", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in your name, email and message before sending.", "error")
        return redirect(url_for("home") + "#contact")

    save_message({
        "name": name,
        "email": email,
        "phone": phone,
        "goal": goal,
        "message": message,
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
    })

    flash(f"Thanks {name.split()[0]}! Our team will reach out within 24 hours.", "success")
    return redirect(url_for("home") + "#contact")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
