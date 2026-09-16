"""Digital flyer for HSG Sailing.

Mobile-only, snap-scrolling one-pager reached by scanning a QR code at the
club fair. Each offering is a card: a 9:16 photo with the title on the front,
the description on the colour-filled back.

Copy lives in content.py, markup in render.py, icons in icons.py.

The whole flyer lives inside ONE html component. Streamlit widgets are avoided
on purpose -- any widget interaction triggers a server rerun, which would reset
the visitor's scroll position mid-flyer.
"""

import streamlit as st
import streamlit.components.v1 as components

from content import PANELS
from render import render_panels

st.set_page_config(page_title="HSG Sailing", layout="wide", initial_sidebar_state="collapsed")

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
  /* Wordmark logo already says "HSG SAILING", so give it room to breathe. */
  .contact-logo { margin-bottom: 1.1rem; }

  .back { transform: rotateY(180deg); }

  /* Darkening layer so text stays readable over a busy photo. The gradient
     itself is set inline per panel, scaled to that photo's brightness. */
  .scrim { position: absolute; inset: 0; }

  .content {
    position: relative;
    z-index: 1;
    padding: 0 2rem;
    text-align: center;
    color: #fff;
    /* min-width: 0 lets this flex item shrink below its longest word, so a
       long compound like "Hochseeausweis" wraps instead of overflowing on a
       narrow screen. Belt and braces with overflow-wrap below. */
    width: 100%;
    max-width: 34rem;
    min-width: 0;
  }

  /* Long compounds (Hochseeausweis, D-Schein) must not overflow. No
     hyphens: auto -- it chopped body copy mid-word on nearly every line. */
  h1, h2, .club, .caption, .body, .offers li, .link-label {
    overflow-wrap: break-word;
  }

  h1 {
    font-size: clamp(1.9rem, 10vw, 3rem);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -0.02em;
    text-wrap: balance;
    text-shadow: 0 2px 18px rgba(0,0,0,.5);
  }

  .caption {
    margin-top: .85rem;
    font-size: clamp(1rem, 4.2vw, 1.15rem);
    line-height: 1.45;
    opacity: .9;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }

  .kicker {
    margin-top: 1.6rem;
    font-size: 1rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    opacity: .8;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }

  /* --- Hero masthead: greeting, logo, club name -------------------------- */
  .hero-content { display: flex; flex-direction: column; align-items: center; }

  .front .greeting {
    margin: 0;
    font-size: clamp(1.35rem, 6.2vw, 1.9rem);
    font-weight: 600;
    letter-spacing: -0.01em;
    opacity: .95;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }

  .hero-logo { width: clamp(4.5rem, 27vw, 7rem); margin: 1.15rem 0 .95rem; }
  .hero-logo img {
    width: 100%; height: auto; display: block;
    filter: drop-shadow(0 3px 14px rgba(0,0,0,.5));
  }

  .club {
    font-size: clamp(2.2rem, 12vw, 3.6rem);
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -0.02em;
  }

  /* --- Card back --------------------------------------------------------- */
  .back-content {
    text-align: left;
    /* Safety valve: if a description ever outgrows a small screen it scrolls
       here rather than being clipped. overscroll-behavior stops that scroll
       from chaining into the deck and snapping to the next panel. */
    max-height: 100%;
    overflow-y: auto;
    overscroll-behavior: contain;
    scrollbar-width: none;
    padding: 4.5rem 2rem 6rem;
  }
  .back-content::-webkit-scrollbar { display: none; }

  .back h2 {
    font-size: clamp(1.5rem, 7vw, 2.05rem);
    line-height: 1.12;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1.1rem;
  }

  .body {
    font-size: clamp(.98rem, 4.2vw, 1.12rem);
    line-height: 1.55;
    opacity: .94;
  }
  .body strong { font-weight: 700; opacity: 1; }

  /* --- Info field ("Free for members" etc.) ------------------------------ */
  .info {
    display: inline-flex;
    align-items: center;
    gap: .55rem;
    margin-top: 1.5rem;
    padding: .6rem .9rem;
    border: 1px solid rgba(255,255,255,.3);
    border-radius: .75rem;
    background: rgba(255,255,255,.13);
    font-size: .88rem;
    font-weight: 600;
    line-height: 1.3;
    text-align: left;
  }
  .info-icon { flex: 0 0 auto; width: 1.15rem; height: 1.15rem; opacity: .95; }
  .info-icon svg { width: 100%; height: 100%; display: block; }

  /* --- Recruiting sticker ------------------------------------------------ */
  .sticker {
    position: absolute;
    z-index: 4;
    top: calc(1.15rem + env(safe-area-inset-top, 0px));
    right: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: .45rem .7rem;
    border-radius: .6rem;
    background: #ffd166;
    color: #1a1c1f;
    transform: rotate(4deg);
    box-shadow: 0 4px 14px rgba(0,0,0,.35);
  }
  .sticker-top {
    font-size: .62rem;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
    opacity: .75;
  }
  .sticker-role { font-size: .85rem; font-weight: 800; letter-spacing: -0.01em; }

  /* --- Additional offerings list ----------------------------------------- */
  .list-content { text-align: left; padding: 0 2rem; }
  .list-title { text-align: left; }
  .list-content .caption { text-align: left; }

  .offers { list-style: none; margin-top: 1.6rem; }
  .offers li {
    position: relative;
    padding-left: 1.6rem;
    margin-bottom: .95rem;
    font-size: clamp(1.02rem, 4.6vw, 1.2rem);
    font-weight: 600;
    line-height: 1.35;
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
  }
  /* Little sail-shaped bullet marker. */
  .offers li::before {
    content: "";
    position: absolute;
    left: .1rem; top: .42em;
    width: 0; height: 0;
    border-left: .45rem solid rgba(255,255,255,.9);
    border-top: .32rem solid transparent;
    border-bottom: .32rem solid transparent;
  }

  /* --- Contact ----------------------------------------------------------- */
  .contact-content { display: flex; flex-direction: column; align-items: center; width: 100%; }
  .contact-logo { width: clamp(3.2rem, 18vw, 4.5rem); margin-bottom: .9rem; }
  .contact-logo img {
    width: 100%; height: auto; display: block;
    filter: drop-shadow(0 3px 14px rgba(0,0,0,.5));
  }
  .contact-title { font-size: clamp(1.7rem, 8.5vw, 2.5rem); }

  .links { width: 100%; margin-top: 1.9rem; display: flex; flex-direction: column; gap: .7rem; }

  .link-row {
    display: flex;
    align-items: center;
    gap: .85rem;
    min-height: 52px;            /* comfortable thumb target */
    padding: .7rem .95rem;
    border: 1px solid rgba(255,255,255,.28);
    border-radius: .85rem;
    background: rgba(255,255,255,.13);
    -webkit-backdrop-filter: blur(6px);
    backdrop-filter: blur(6px);
    color: #fff;
    text-decoration: none;
  }
  .link-row:active { background: rgba(255,255,255,.26); }

  .link-icon { flex: 0 0 auto; width: 1.4rem; height: 1.4rem; }
  .link-icon svg { width: 100%; height: 100%; display: block; }
  .icon-insta { color: #f7a8c4; }
  .icon-whatsapp { color: #6ee7a8; }

  .link-label {
    flex: 1 1 auto;
    text-align: left;
    font-size: .98rem;
    font-weight: 600;
    word-break: break-word;
  }
  .link-chevron { flex: 0 0 auto; opacity: .55; font-size: 1.1rem; }

  /* --- The tap target ---------------------------------------------------- */
  .pill {
    position: absolute;
    bottom: calc(3.4rem + env(safe-area-inset-bottom, 0px));
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
    cursor: pointer;
    min-height: 44px;            /* Apple's minimum touch target */
  }
  .pill:active { background: rgba(255,255,255,.3); }

  /* Nudge the first "More info" so visitors learn cards are tappable. */
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
    display: flex; flex-direction: column; gap: .45rem;
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

FLYER = FLYER_TEMPLATE.replace("__PANELS__", render_panels(PANELS))

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
