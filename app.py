"""Digital flyer for the university sailing club.

Mobile-only, snap-scrolling one-pager. Each panel is a card: a 9:16 photo with
a title on the front, a few bullet points on the colour-filled back.

The whole flyer lives inside ONE html component. Streamlit widgets are avoided
on purpose -- any widget interaction triggers a server rerun, which would reset
the visitor's scroll position mid-flyer.
"""

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sailing Club", layout="wide", initial_sidebar_state="collapsed")

IMAGES = Path(__file__).parent / "images"

# --- Content ------------------------------------------------------------------
# `image` is the slug of images/<slug>.9x16.jpg. `color` tints the card back.
PANELS = [
    {
        "key": "welcome",
        "greeting": "Welcome aboard!",
        "club": "HSG Sailing",
        "text": "Scroll down",
        "color": "#0b3d6b",
        "hero": True,          # hero panel has no back face
    },
    {
        "key": "beginner",
        "title": "Beginner friendly",
        "text": "Never touched a tiller? Perfect.",
        "color": "#124e78",
        "bullets": [
            "No experience needed &mdash; we start on land",
            "Boats, lifejackets and gear all provided",
            "Your first taster sail is free",
            "Intro evening every second Tuesday",
        ],
    },
    {
        "key": "theory",
        "title": "Theory courses",
        "text": "Learn the why, not just the how.",
        "color": "#0f5c58",
        "bullets": [
            "Knots, right of way and weather basics",
            "Wednesday evenings on campus",
            "Optional licence exam prep",
            "Course notes free for members",
        ],
    },
    {
        "key": "offshore",
        "title": "Offshore turns",
        "text": "A week at sea with the crew.",
        "color": "#123f55",
        "bullets": [
            "One week aboard a 40ft yacht",
            "Baltic in spring, Mediterranean in autumn",
            "Split into watches &mdash; you really helm",
            "Costs shared, kept student friendly",
        ],
    },
    {
        "key": "regatta",
        "title": "Regatta",
        "text": "Race other universities.",
        "color": "#6b2d12",
        "bullets": [
            "Casual club races most weekends",
            "University championships each term",
            "Team racing in matched boats",
            "Coaching from experienced helms",
        ],
    },
    {
        "key": "events",
        "title": "Events",
        "text": "The bit that isn't sailing.",
        "color": "#3f2168",
        "bullets": [
            "Barbecues down at the boathouse",
            "Boat maintenance weekends",
            "Pub nights after training",
            "The end-of-season party",
        ],
    },
]

# Placeholder logo: transparent inline SVG. Swap for the club's own SVG.
LOGO = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M52 6 L52 78 L90 78 Z" fill="#ffffff" opacity="0.95"/>
  <path d="M46 26 L46 78 L14 78 Z" fill="#ffffff" opacity="0.7"/>
  <path d="M6 84 q22 10 44 0 q22 -10 44 0 l0 8 q-22 -10 -44 0 q-22 10 -44 0 Z" fill="#ffffff" opacity="0.9"/>
</svg>
"""


@st.cache_data(show_spinner=False)
def photo_data_uri(slug: str) -> str:
    """Inline a photo as base64.

    The component runs in a srcdoc iframe, so relative file paths do not
    resolve -- inlining is what makes the photos show up both locally and on
    Community Cloud.
    """
    path = IMAGES / f"{slug}.9x16.jpg"
    if not path.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def render_panel(panel: dict, index: int, total: int) -> str:
    title = panel.get("title", "").replace("{logo}", LOGO)
    photo = photo_data_uri(panel["key"])
    background = f"url('{photo}')" if photo else panel["color"]
    dots = "".join(
        f'<i class="{"on" if i == index else ""}"></i>' for i in range(total)
    )

    if panel.get("hero"):
        # Hero panel: no flip, just the masthead and the nudge to scroll.
        return f"""
        <section class="panel">
          <div class="card">
            <div class="face front" style="background-image: {background};">
              <div class="scrim"></div>
              <div class="content hero-content">
                <p class="greeting">{panel["greeting"]}</p>
                <div class="hero-logo">{LOGO}</div>
                <h1 class="club">{panel["club"]}</h1>
                <p class="kicker">{panel["text"]}</p>
              </div>
              <div class="arrow" aria-hidden="true">&#8964;</div>
            </div>
          </div>
          <div class="dots" aria-hidden="true">{dots}</div>
        </section>
        """

    bullets = "".join(f"<li>{b}</li>" for b in panel.get("bullets", []))
    return f"""
    <section class="panel">
      <div class="card" id="card-{index}">
        <div class="face front" style="background-image: {background};">
          <div class="scrim"></div>
          <div class="content">
            <h1>{title}</h1>
            <p>{panel["text"]}</p>
          </div>
          <button class="pill" data-flip="{index}" aria-expanded="false"
                  aria-label="More about {panel["title"]}">
            More info <span aria-hidden="true">&#8250;</span>
          </button>
        </div>
        <div class="face back" style="background: {panel["color"]};">
          <div class="content back-content">
            <h2>{panel["title"]}</h2>
            <ul>{bullets}</ul>
          </div>
          <button class="pill" data-flip="{index}" aria-label="Back to photo">
            <span aria-hidden="true">&#8249;</span> Back
          </button>
        </div>
      </div>
      <div class="dots" aria-hidden="true">{dots}</div>
    </section>
    """


PANELS_HTML = "".join(render_panel(p, i, len(PANELS)) for i, p in enumerate(PANELS))

# Plain (non-f) template so CSS/JS braces need no escaping.
FLYER_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

  html, body {
    height: 100%;
    overflow: hidden;
    background: #000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  /* The snap container: the only thing that scrolls. */
  .deck {
    height: var(--vh, 100dvh);
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .deck::-webkit-scrollbar { display: none; }

  .panel {
    position: relative;
    height: var(--vh, 100dvh);
    scroll-snap-align: start;
    scroll-snap-stop: always;   /* never skip a panel on a fast flick */
    overflow: hidden;
    perspective: 1400px;        /* gives the flip its depth */
  }

  /* --- The flip card ------------------------------------------------------ */
  .card {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.65s cubic-bezier(0.4, 0.05, 0.2, 1);
  }
  .card.flipped { transform: rotateY(180deg); }

  .face {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;   /* iOS needs the prefix */

    /* backface-visibility alone is not enough: Safari leaks descendants of a
       hidden face through when a child makes its own rendering context (our
       text-shadows, the pill's backdrop-filter), so the front's title showed
       up mirrored on the back. Hiding the inactive face outright is reliable.
       visibility does not interpolate, so with a delay of half the flip it
       switches exactly when the card is edge-on and invisible anyway. */
    visibility: visible;
    transition: visibility 0s linear 0.33s;
  }
  .face * { backface-visibility: hidden; -webkit-backface-visibility: hidden; }

  .back { visibility: hidden; }
  .card.flipped .front { visibility: hidden; }
  .card.flipped .back { visibility: visible; }

  .front {
    background-size: cover;
    background-position: center;
    background-color: #0b3d6b;   /* shows while the photo decodes */
  }

  .back { transform: rotateY(180deg); }   /* visibility rules are above */

  /* Darkening layer so text stays readable over a busy photo. */
  .scrim {
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,.5) 0%, rgba(0,0,0,.28) 45%, rgba(0,0,0,.68) 100%);
  }

  .content {
    position: relative;
    z-index: 1;
    padding: 0 2rem;
    text-align: center;
    color: #fff;
    max-width: 34rem;
  }

  h1 {
    font-size: clamp(2rem, 11vw, 3.2rem);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -0.02em;
    text-wrap: balance;
    text-shadow: 0 2px 18px rgba(0,0,0,.5);
  }

  .front p {
    margin-top: .9rem;
    font-size: clamp(1rem, 4.2vw, 1.15rem);
    line-height: 1.5;
    opacity: .9;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }

  .kicker {
    margin-top: 1.6rem !important;
    font-size: 1rem !important;
    letter-spacing: .12em;
    text-transform: uppercase;
    opacity: .8;
  }

  .logo { display: inline-block; width: 1.05em; height: 1.05em; vertical-align: -.12em; margin: 0 .12em; }
  .logo svg { width: 100%; height: 100%; display: block; filter: drop-shadow(0 2px 8px rgba(0,0,0,.45)); }

  /* --- Hero masthead: greeting, logo, club name -------------------------- */
  .hero-content { display: flex; flex-direction: column; align-items: center; }

  .front .greeting {
    margin: 0;
    font-size: clamp(1.35rem, 6.2vw, 1.9rem);
    font-weight: 600;
    letter-spacing: -0.01em;
    opacity: .95;
  }

  .hero-logo {
    width: clamp(4.5rem, 27vw, 7rem);
    margin: 1.15rem 0 .95rem;
  }
  .hero-logo svg {
    width: 100%; height: auto; display: block;
    filter: drop-shadow(0 3px 14px rgba(0,0,0,.5));
  }

  .club {
    font-size: clamp(2.2rem, 12vw, 3.6rem);
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -0.02em;
    text-wrap: balance;
    text-shadow: 0 2px 18px rgba(0,0,0,.5);
  }

  /* --- Card back --------------------------------------------------------- */
  .back-content { text-align: left; }

  .back h2 {
    font-size: clamp(1.6rem, 7.5vw, 2.2rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1.4rem;
  }

  .back ul { list-style: none; }

  .back li {
    position: relative;
    padding-left: 1.6rem;
    margin-bottom: 1rem;
    font-size: clamp(1rem, 4.4vw, 1.15rem);
    line-height: 1.45;
    opacity: .95;
  }

  /* Little sail-shaped bullet marker. */
  .back li::before {
    content: "";
    position: absolute;
    left: .1rem; top: .45em;
    width: 0; height: 0;
    border-left: .42rem solid rgba(255,255,255,.85);
    border-top: .3rem solid transparent;
    border-bottom: .3rem solid transparent;
  }

  /* --- The tap target ---------------------------------------------------- */
  .pill {
    position: absolute;
    bottom: 3.4rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .75rem 1.4rem;
    border: 1px solid rgba(255,255,255,.45);
    border-radius: 999px;
    background: rgba(255,255,255,.16);
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
    color: #fff;
    font: inherit;
    font-size: .95rem;
    font-weight: 600;
    letter-spacing: .01em;
    cursor: pointer;
    /* Comfortable thumb target: Apple's 44pt minimum. */
    min-height: 44px;
  }
  .pill:active { background: rgba(255,255,255,.3); }

  /* Nudge the very first "More info" so visitors learn cards are tappable. */
  #card-1 .front .pill { animation: hint 2.6s ease-in-out 1.2s 3; }
  @keyframes hint {
    0%, 100% { transform: translateX(-50%) scale(1); }
    50%      { transform: translateX(-50%) scale(1.07); }
  }

  .arrow {
    position: absolute; bottom: 4.2rem; left: 0; right: 0;
    z-index: 1; text-align: center; color: #fff; font-size: 2rem; opacity: .75;
    animation: bob 1.8s ease-in-out infinite;
  }
  @keyframes bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(8px); } }

  /* Progress dots, outside the card so they do not flip with it. */
  .dots {
    position: absolute; z-index: 3;
    right: 1rem; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: .5rem;
  }
  .dots i { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.35); }
  .dots i.on { background: #fff; }

  @media (prefers-reduced-motion: reduce) {
    .card { transition: none; }
    .face { transition: none; }
    .arrow, #card-1 .front .pill { animation: none; }
  }
</style>
</head>
<body>
  <div class="deck" id="deck">
    __PANELS__
  </div>

  <script>
    /* Size the flyer to the REAL viewport rather than trusting Streamlit's
       fixed iframe height. `100dvh` inside an iframe resolves against the
       iframe's own box, so a 900px iframe gives 900px panels on a 760px
       phone: text sits below centre and the bottom gets clipped. Measuring
       the parent window avoids depending on Streamlit's internal class names. */
    function fit() {
      var h = window.innerHeight;
      try {
        if (window.parent && window.parent !== window && window.parent.innerHeight) {
          h = window.parent.innerHeight;
        }
      } catch (e) { /* cross-origin: fall back to our own height */ }

      document.documentElement.style.setProperty('--vh', h + 'px');

      try {
        var fe = window.frameElement;
        if (fe) { fe.style.height = h + 'px'; fe.style.width = '100vw'; }
      } catch (e) {}
    }

    fit();
    addEventListener('resize', fit);
    addEventListener('orientationchange', fit);
    try { window.parent.addEventListener('resize', fit); } catch (e) {}
    [100, 500, 1500].forEach(function (d) { setTimeout(fit, d); });

    /* --- Flip handling --------------------------------------------------- */
    document.querySelectorAll('[data-flip]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var card = document.getElementById('card-' + btn.dataset.flip);
        if (!card) return;
        var nowFlipped = card.classList.toggle('flipped');
        var front = card.querySelector('.front .pill');
        if (front) front.setAttribute('aria-expanded', nowFlipped ? 'true' : 'false');
      });
    });

    /* Scrolling away resets a card, so nobody scrolls back to a stray back face. */
    if ('IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.intersectionRatio < 0.4) {
            entry.target.classList.remove('flipped');
            var front = entry.target.querySelector('.front .pill');
            if (front) front.setAttribute('aria-expanded', 'false');
          }
        });
      }, { root: document.getElementById('deck'), threshold: [0, 0.4, 1] });
      document.querySelectorAll('.card').forEach(function (c) { obs.observe(c); });
    }
  </script>
</body>
</html>
"""

FLYER = FLYER_TEMPLATE.replace("__PANELS__", PANELS_HTML)

# --- Strip all Streamlit chrome and let the component fill the whole screen ---
# NB: these data-testid / iframe title values are Streamlit internals and can be
# renamed between versions. If the flyer ever stops filling the screen, re-check
# them first -- that is exactly what broke mobile the first time round.
st.markdown(
    """
    <style>
      #MainMenu, header, footer, [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      [data-testid="stBottom"],
      /* Community Cloud host chrome: "Manage app" and the Streamlit badge.
         These are injected by the host, not the OSS build, so the selectors
         are best-effort and may need revisiting. */
      [data-testid="stAppDeployButton"], [data-testid="manage-app-button"],
      .viewerBadge_container__1QSob, .viewerBadge_link__qRIco,
      a[href*="streamlit.io/cloud"], iframe[title="streamlitApp"] { display: none !important; }

      /* No white gap under the flyer if anything is ever shorter than the screen. */
      body, .stApp { background: #000 !important; }

      html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        height: 100dvh !important;
        overflow: hidden !important;
      }

      /* Kill the default page padding that would push the flyer down the screen. */
      .block-container,
      [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"],
      [data-testid="stVerticalBlockBorderWrapper"] { gap: 0 !important; }

      iframe[title="st.iframe"],
      [data-testid="stIFrame"],
      [data-testid="stCustomComponentV1"] {
        height: 100dvh !important;
        width: 100vw !important;
        display: block !important;
        border: none !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(FLYER, height=900, scrolling=False)
