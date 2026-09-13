import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sailing Club", layout="wide", initial_sidebar_state="collapsed")

# --- Panels: swap `color` for a background image later (see README) -----------
PANELS = [
    {
        "title": 'Welcome to the <span class="logo">{logo}</span> sailing club!',
        "text": "Scroll down",
        "color": "#0b3d6b",
        "hero": True,
    },
    {
        "title": "Beginner friendly",
        "text": "Never touched a tiller? Perfect. We teach you from scratch — no experience, no own boat, no problem.",
        "color": "#1b6ca8",
    },
    {
        "title": "Theory courses",
        "text": "Right of way, knots, weather and navigation. Evening sessions on campus over the winter term.",
        "color": "#0f766e",
    },
    {
        "title": "Offshore turns",
        "text": "A week on a yacht with the crew. Baltic and Mediterranean trips every semester break.",
        "color": "#155e75",
    },
    {
        "title": "Regatta",
        "text": "Race against other universities. Casual club races on weekends, proper championships if you catch the bug.",
        "color": "#7c2d12",
    },
    {
        "title": "Events",
        "text": "Barbecues, boat maintenance days, pub nights and the legendary end-of-season party.",
        "color": "#4c1d95",
    },
]

# Placeholder logo: transparent inline SVG (a little sail). Replace with your own.
LOGO = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-label="logo">
  <path d="M52 6 L52 78 L90 78 Z" fill="#ffffff" opacity="0.95"/>
  <path d="M46 26 L46 78 L14 78 Z" fill="#ffffff" opacity="0.7"/>
  <path d="M6 84 q22 10 44 0 q22 -10 44 0 l0 8 q-22 -10 -44 0 q-22 10 -44 0 Z" fill="#ffffff" opacity="0.9"/>
</svg>
"""

def build_panel(p, index):
    title = p["title"].replace("{logo}", LOGO) if "{logo}" in p["title"] else p["title"]
    hero = " hero" if p.get("hero") else ""
    arrow = '<div class="arrow">&#8964;</div>' if p.get("hero") else ""
    return f"""
    <section class="panel{hero}" style="--bg: {p['color']};">
      <div class="scrim"></div>
      <div class="content">
        <h1>{title}</h1>
        <p>{p['text']}</p>
      </div>
      {arrow}
      <div class="dots">{''.join(
          f'<i class="{"on" if i == index else ""}"></i>' for i in range(len(PANELS))
      )}</div>
    </section>
    """

FLYER = f"""
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}

  html, body {{
    height: 100%;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #000;
  }}

  /* The snap container: this is the only thing that scrolls. */
  .deck {{
    height: 100dvh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }}
  .deck::-webkit-scrollbar {{ display: none; }}

  .panel {{
    position: relative;
    height: 100dvh;
    scroll-snap-align: start;
    scroll-snap-stop: always;   /* never skip past a panel on a fast flick */
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Stand-in for the photo. Replace `background` with your image, see README. */
    background: var(--bg);
    background-size: cover;
    background-position: center;
  }}

  /* Darkening layer so text stays readable over a busy photo. */
  .scrim {{
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,.25) 45%, rgba(0,0,0,.6) 100%);
  }}

  .content {{
    position: relative;
    z-index: 1;
    padding: 0 2rem;
    text-align: center;
    color: #fff;
    max-width: 34rem;
  }}

  h1 {{
    font-size: clamp(2rem, 11vw, 3.2rem);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -0.02em;
    text-wrap: balance;
    text-shadow: 0 2px 18px rgba(0,0,0,.5);
  }}

  p {{
    margin-top: 1rem;
    font-size: clamp(1rem, 4.4vw, 1.2rem);
    line-height: 1.5;
    opacity: .92;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }}

  .hero p {{ margin-top: 1.6rem; font-size: 1rem; letter-spacing: .12em; text-transform: uppercase; opacity: .8; }}

  /* Inline transparent logo sitting in the headline. */
  .logo {{ display: inline-block; width: 1.05em; height: 1.05em; vertical-align: -.12em; margin: 0 .12em; }}
  .logo svg {{ width: 100%; height: 100%; display: block; filter: drop-shadow(0 2px 8px rgba(0,0,0,.45)); }}

  .arrow {{
    position: absolute; bottom: 4.2rem; left: 0; right: 0;
    z-index: 1; text-align: center; color: #fff; font-size: 2rem; opacity: .75;
    animation: bob 1.8s ease-in-out infinite;
  }}
  @keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(8px); }} }}

  /* Progress dots so people know how much flyer is left. */
  .dots {{
    position: absolute; z-index: 1;
    right: 1rem; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: .5rem;
  }}
  .dots i {{ width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.35); }}
  .dots i.on {{ background: #fff; }}

  @media (prefers-reduced-motion: reduce) {{ .arrow {{ animation: none; }} }}
</style>
</head>
<body>
  <div class="deck">
    {''.join(build_panel(p, i) for i, p in enumerate(PANELS))}
  </div>
</body>
</html>
"""

# --- Strip all Streamlit chrome and let the component fill the whole screen ---
st.markdown(
    """
    <style>
      #MainMenu, header, footer, [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
      .stApp { overflow: hidden !important; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      iframe[title="streamlit.components.v1.html"],
      iframe[title="streamlitApp"], .stCustomComponentV1 {
        height: 100dvh !important;
        width: 100vw !important;
        display: block;
        border: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(FLYER, height=900, scrolling=False)
