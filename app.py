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
    "name": "Feral Fitness",
    "tagline": "Fitness made fun & easy",
    "subtitle": "Beginner-friendly programs: Yoga, Zumba, Aerobics, CrossFit, HIIT, Dance.",
    "phone_display": "096008 83838",
    # country code + number, no + or spaces (remove leading zero)
    "whatsapp_number": "919600883838",
    "email": "hello@feralfitness.com",
    "address": "Feral fitness, new number 44, 2nd floor above Kotak Mahindra Bank ATM, near five lights junction, West Mambalam, Chennai, Tamil Nadu 600024",
    "hours": [
        {"days": "Daily", "time": "Open – Closes 10:00 PM"},
    ],
    "instagram": "https://instagram.com/feralfitness",
    "facebook": "https://facebook.com/feralfitness",
    "youtube": "https://youtube.com/feralfitness",
}

WHATSAPP_DEFAULT_MESSAGE = f"Hi {SITE['name']}, I'd like to know more about your membership plans."

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
    {"icon": "spa", "title": "Yoga & Mobility", "desc": "Beginner-friendly yoga classes to improve flexibility and recovery."},
    {"icon": "music", "title": "Zumba & Dance Fitness", "desc": "High-energy dance classes including Zumba and dance cardio."},
    {"icon": "heart-pulse", "title": "Aerobics & Cardio", "desc": "Group aerobics and endurance sessions to boost stamina."},
    {"icon": "dumbbell", "title": "Strength & Conditioning", "desc": "Structured strength programs, CrossFit-style WODs and functional training."},
    {"icon": "bolt", "title": "HIIT", "desc": "Short, intense interval training sessions for fast results."},
    {"icon": "users", "title": "Dedicated Kids Program", "desc": "Kids classes: Yoga, Gymnastics, Karate and Dance — safe, fun and age-appropriate."},
    {"icon": "person-chalkboard", "title": "Expert Coaches", "desc": "Professional trainers guiding beginners and experienced members alike."},
]

TESTIMONIALS = [
    {"name": "Sanjana S", "role": "Member",
     "quote": "Best gym have ever gone..good ambience ,professional trainers and best service"},
    {"name": "Sri Sankara Narayanan", "role": "Member",
     "quote": "Very very hygienic flooor and good atmosphere to work out."},
    {"name": "Kirubhahar Praveen", "role": "Member",
     "quote": "Would love to be a regular here, great warmth and vibes in the place."},
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
