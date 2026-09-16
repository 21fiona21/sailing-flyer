"""Turns content.PANELS into the flyer's HTML."""

import base64
from functools import lru_cache
from pathlib import Path

from PIL import Image

from icons import ICONS, logo_img

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


def _darken(hex_colour: str, factor: float = 0.55) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * factor), int(g * factor), int(b * factor))


def _background(panel: dict) -> str:
    photo = photo_data_uri(panel.get("image", ""))
    if photo:
        return f"url('{photo}')"
    # No photo: a deep gradient field rather than a flat block of colour.
    return f'linear-gradient(165deg, {panel["color"]} 0%, {_darken(panel["color"])} 100%)'


@lru_cache(maxsize=None)
def _central_luminance(slug: str):
    """Mean brightness of the band where the headline sits, 0-255."""
    path = IMAGES / f"{slug}.9x16.jpg"
    if not path.exists():
        return None
    im = Image.open(path).convert("L")
    band = im.crop((0, int(im.height * 0.30), im.width, int(im.height * 0.70)))
    return sum(band.getdata()) / (band.width * band.height)


def _scrim(panel: dict, extra: float = 0.0) -> str:
    """Darkening layer, scaled to how bright the photo actually is.

    Measured rather than eyeballed: most of the club's photos are bright sky
    and water right where the white headline goes, and a fixed scrim either
    washed out the dark ones or left the bright ones unreadable.
    """
    if not panel.get("image"):
        return ""            # gradient panels need no scrim
    lum = _central_luminance(panel["image"])
    if lum is None:
        base = 0.42
    else:
        t = max(0.0, min(1.0, (lum - 90) / 95))      # 90 -> 0, 185 -> 1
        base = 0.42 + t * 0.28
    base = min(0.82, base + extra)
    top, mid, bot = min(0.9, base + 0.06), base, min(0.92, base + 0.16)
    return ('<div class="scrim" style="background: linear-gradient(180deg, '
            f'rgba(0,0,0,{top:.2f}) 0%, rgba(0,0,0,{mid:.2f}) 45%, '
            f'rgba(0,0,0,{bot:.2f}) 100%);"></div>')


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
          {_scrim(panel)}
          <div class="content hero-content">
            <p class="greeting">{panel["greeting"]}</p>
            <div class="hero-logo">{logo_img("mark")}</div>
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
          {_scrim(panel)}
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
          {_scrim(panel, extra=0.12)}
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
          {_scrim(panel, extra=0.12)}
          <div class="content contact-content">
            <div class="contact-logo">{logo_img("full")}</div>
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
