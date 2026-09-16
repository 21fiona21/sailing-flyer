"""Flyer content: edit this file to change what the flyer says.

Keys:
  type    "hero" | "flip" | "list" | "contact"
  image   slug of images/<slug>.9x16.jpg
  title   shown on the card front, and again on the back
  caption short line under the title on the front
  body    back-of-card text; <strong> marks the keywords worth scanning
  info    the "free for members" style line, rendered as an info field
  hiring  adds a recruiting sticker to both faces
"""

PANELS = [
    {
        "type": "hero",
        "image": "hero",
        "greeting": "Welcome aboard!",
        "club": "HSG Sailing",
        "text": "Scroll down",
        "color": "#0b3d6b",
    },
    {
        "type": "flip",
        "image": "weekly",
        "title": "Weekly Sailing Sessions",
        "caption": "Every Saturday on Lake Constance",
        "body": (
            "Join our weekly sailing sessions <strong>every Saturday</strong> during the "
            "semester from <strong>2&ndash;5 pm</strong> in <strong>Staad on Lake "
            "Constance</strong>, just 20 minutes from St. Gallen. Sailors of "
            "<strong>all levels</strong> are welcome, from complete beginners to "
            "experienced sailors. <strong>No sailing licence or previous experience "
            "is required.</strong>"
        ),
        "info": "Free for members",
        "color": "#124e78",
    },
    {
        "type": "flip",
        "image": "theory-beginner",
        "title": "Beginner Theory Course",
        "caption": "Two evenings, from wind to knots",
        "body": (
            "Learn how sailing actually works! Over <strong>two evening sessions on "
            "campus</strong>, we cover everything from <strong>wind, points of sail "
            "and sail trim</strong> to essential <strong>manoeuvres</strong>, "
            "<strong>right-of-way rules</strong> and <strong>nautical knots</strong>."
        ),
        "info": "Free for members, materials provided",
        "color": "#0f5c58",
    },
    {
        "type": "flip",
        "image": "theory-hochsee",
        "title": "Hochseeausweis Theory Course",
        "caption": "One intensive day, offshore ready",
        "body": (
            "Prepare for the theoretical <strong>Hochseeausweis exam</strong> in our "
            "<strong>one-day intensive workshop</strong>. Work through the required "
            "topics in <strong>offshore navigation</strong>, with a focus on "
            "<strong>nautical chartwork</strong>, <strong>tidal calculations</strong> "
            "and the relevant concepts and calculations."
        ),
        "info": "Free for members, materials provided",
        "color": "#14415c",
    },
    {
        "type": "flip",
        "image": "lago",
        "title": "Lago Maggiore Weekend Trip",
        "caption": "A weekend of Italian flair",
        "body": (
            "Spend a weekend sailing across beautiful <strong>Lago Maggiore</strong>, "
            "exploring both the <strong>Swiss and Italian</strong> sides of the lake. "
            "Discover <strong>picturesque towns and islands</strong>, take in the "
            "Italian flair and enjoy plenty of <strong>time on the water</strong> to "
            "practise your sailing skills."
        ),
        "info": "Members-only, additional fees apply",
        "color": "#15614a",
    },
    {
        "type": "flip",
        "image": "offshore",
        "title": "Offshore Turns",
        "caption": "Week-long trips, real sea miles",
        "body": (
            "Take your sailing <strong>beyond inland waters</strong> and join us for "
            "<strong>week-long trips</strong> in exciting destinations. <strong>Live "
            "and sail together as a crew</strong>, explore new sailing areas and gain "
            "hands-on <strong>offshore experience</strong> along the way."
        ),
        "info": "Members-only, additional fees apply",
        "color": "#123f55",
    },
    {
        "type": "flip",
        "image": "regatta",
        "title": "Regatta",
        "caption": "Race with the HSG team",
        "body": (
            "Interested in racing? Join other HSG Sailing members for "
            "<strong>regattas</strong> and opportunities to practise <strong>competitive "
            "sailing</strong>. You don&rsquo;t need previous racing experience, but should "
            "have a <strong>solid sailing background</strong> and be motivated to "
            "<strong>learn, contribute and become part of the team</strong>."
        ),
        "info": "Members-only, additional fees apply",
        "color": "#6b2d12",
        "hiring": "Head of Regatta",
    },
    {
        "type": "flip",
        "image": "events",
        "title": "Events &amp; Community",
        "caption": "More than just sailing",
        "body": (
            "HSG Sailing is about <strong>more than just sailing!</strong> Join us for "
            "<strong>sports parties, club regattas, Christmas parties, summer "
            "barbecues</strong> and other events throughout the year. Meet fellow "
            "sailing and watersports enthusiasts and become part of our "
            "<strong>active community</strong>."
        ),
        "color": "#3f2168",
    },
    {
        "type": "list",
        "image": "offerings",
        "title": "Additional Offerings",
        "caption": "Organised by demand &mdash; just ask us",
        "bullets": [
            "Manoeuvre Trainings",
            "Theory &amp; Practice Crash Course",
            "D-Schein Prep Sessions",
            "D-Schein &amp; Hochseeausweis Info Events",
        ],
        "info": "All free for members",
        "color": "#1b4f6b",
    },
    {
        "type": "contact",
        "title": "Come sail with us",
        "caption": "See you on the water!",
        "links": [
            {"icon": "web",      "label": "hsgsailing.ch",   "href": "https://hsgsailing.ch"},
            {"icon": "mail",     "label": "hsgsailing@gmail.com", "href": "mailto:hsgsailing@gmail.com"},
            {"icon": "insta",    "label": "@hsgsailing",     "href": "https://instagram.com/hsgsailing"},
            {"icon": "whatsapp", "label": "Join our WhatsApp community",
             "href": "https://chat.whatsapp.com/EPEfSnyfGcIInBHjwGSglF"},
        ],
        "color": "#0b3d6b",
    },
]
