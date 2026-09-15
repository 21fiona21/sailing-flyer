"""Turns content.PANELS into the flyer's HTML."""

import base64
from pathlib import Path

from icons import ICONS, LOGO

IMAGES = Path(__file__).parent / "images"


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


def _background(panel: dict) -> str:
    photo = photo_data_uri(panel.get("image", ""))
    return f"url('{photo}')" if photo else panel["color"]


def _dots(index: int, total: int) -> str:
    inner = "".join(f'<i class="{"on" if i == index else ""}"></i>' for i in range(total))
    return f'<div class="dots" aria-hidden="true">{inner}</div>'


def _info_field(panel: dict) -> str:
    """The 'Free for members' style line, as a uniform info field."""
    text = panel.get("info")
    if not text:
        return ""
    kind = "free" if text.lower().startswith(("free", "all free")) else "members"
    return (f'<div class="info"><span class="info-icon">{ICONS[kind]}</span>'
            f"<span>{text}</span></div>")


def _sticker(panel: dict) -> str:
    """Recruiting sticker, shown on both faces of a card."""
    role = panel.get("hiring")
    if not role:
        return ""
    return (f'<div class="sticker"><span class="sticker-top">We&rsquo;re hiring</span>'
            f'<span class="sticker-role">{role}</span></div>')


def _hero(panel: dict, index: int, total: int) -> str:
    return f"""
    <section class="panel">
      <div class="card">
        <div class="face front" style="background-image: {_background(panel)};">
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
      {_dots(index, total)}
    </section>
    """


def _flip(panel: dict, index: int, total: int) -> str:
    sticker = _sticker(panel)
    return f"""
    <section class="panel">
      <div class="card" id="card-{index}">
        <div class="face front" style="background-image: {_background(panel)};">
          <div class="scrim"></div>
          {sticker}
          <div class="content">
            <h1>{panel["title"]}</h1>
            <p class="caption">{panel["caption"]}</p>
          </div>
          <button class="pill" data-flip="{index}" aria-expanded="false">
            More info <span aria-hidden="true">&#8250;</span>
          </button>
        </div>
        <div class="face back" style="background: {panel["color"]};">
          {sticker}
          <div class="content back-content">
            <h2>{panel["title"]}</h2>
            <p class="body">{panel["body"]}</p>
            {_info_field(panel)}
          </div>
          <button class="pill" data-flip="{index}">
            <span aria-hidden="true">&#8249;</span> Back
          </button>
        </div>
      </div>
      {_dots(index, total)}
    </section>
    """


def _list(panel: dict, index: int, total: int) -> str:
    bullets = "".join(f"<li>{b}</li>" for b in panel["bullets"])
    return f"""
    <section class="panel">
      <div class="card">
        <div class="face front" style="background-image: {_background(panel)};">
          <div class="scrim scrim-strong"></div>
          <div class="content list-content">
            <h1 class="list-title">{panel["title"]}</h1>
            <p class="caption">{panel["caption"]}</p>
            <ul class="offers">{bullets}</ul>
            {_info_field(panel)}
          </div>
        </div>
      </div>
      {_dots(index, total)}
    </section>
    """


def _contact(panel: dict, index: int, total: int) -> str:
    rows = "".join(
        f'<a class="link-row" href="{l["href"]}" target="_blank" rel="noopener noreferrer">'
        f'<span class="link-icon icon-{l["icon"]}">{ICONS[l["icon"]]}</span>'
        f'<span class="link-label">{l["label"]}</span>'
        f'<span class="link-chevron" aria-hidden="true">&#8250;</span></a>'
        for l in panel["links"]
    )
    return f"""
    <section class="panel">
      <div class="card">
        <div class="face front" style="background-image: {_background(panel)};">
          <div class="scrim scrim-strong"></div>
          <div class="content contact-content">
            <div class="contact-logo">{LOGO}</div>
            <h1 class="contact-title">{panel["title"]}</h1>
            <p class="caption">{panel["caption"]}</p>
            <div class="links">{rows}</div>
          </div>
        </div>
      </div>
      {_dots(index, total)}
    </section>
    """


RENDERERS = {"hero": _hero, "flip": _flip, "list": _list, "contact": _contact}


def render_panels(panels: list) -> str:
    total = len(panels)
    return "".join(
        RENDERERS[p["type"]](p, i, total) for i, p in enumerate(panels)
    )
