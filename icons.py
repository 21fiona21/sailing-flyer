"""Inline SVG icons. Inline so the flyer stays a single self-contained page."""

# Club logo, rebuilt as white artwork on transparency. The SVG the club
# supplied wrapped a raster whose alpha came from luminance, which made the
# background opaque and knocked the artwork out -- a white box on screen.
# logo-mark is the roundel alone; logo-full includes the "HSG SAILING" wordmark.
import base64
from pathlib import Path

_ASSETS = Path(__file__).parent / "assets"


def _png_uri(name: str) -> str:
    path = _ASSETS / name
    if not path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def logo_img(variant: str = "mark", css_class: str = "") -> str:
    """<img> for the club logo. variant is "mark" or "full"."""
    uri = _png_uri(f"logo-{variant}.png")
    cls = f' class="{css_class}"' if css_class else ""
    return f'<img src="{uri}" alt="HSG Sailing"{cls}>'


_STROKE = ('viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"')

ICONS = {
    # Info-field markers
    "free": f'<svg {_STROKE}><circle cx="12" cy="12" r="9"/><path d="M8.2 12.4l2.5 2.4 5-5.6"/></svg>',
    "members": f'<svg {_STROKE}><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/>'
               f'<circle cx="12" cy="7.8" r="1.05" fill="currentColor" stroke="none"/></svg>',

    # Contact links
    "web": f'<svg {_STROKE}><circle cx="12" cy="12" r="9"/><path d="M3.2 12h17.6"/>'
           f'<path d="M12 3c2.8 3.4 2.8 14.6 0 18M12 3c-2.8 3.4-2.8 14.6 0 18"/></svg>',
    "mail": f'<svg {_STROKE}><rect x="2.6" y="5" width="18.8" height="14" rx="2.6"/>'
            f'<path d="M3.4 7.3l8.6 5.7 8.6-5.7"/></svg>',
    "insta": f'<svg {_STROKE}><rect x="3" y="3" width="18" height="18" rx="5.2"/>'
             f'<circle cx="12" cy="12" r="4.1"/>'
             f'<circle cx="17.3" cy="6.7" r="1.15" fill="currentColor" stroke="none"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                '<path d="M12 2.2a9.8 9.8 0 0 0-8.3 15l-1.4 5 5.1-1.35A9.8 9.8 0 1 0 12 2.2zm0 2a7.8 7.8'
                ' 0 1 1-4 14.5l-.37-.22-2.83.75.76-2.77-.22-.37A7.8 7.8 0 0 1 12 4.2z"/>'
                '<path d="M9.05 7.4c.3 0 .5.13.66.5l.66 1.55c.1.25.05.48-.14.66l-.4.42c-.2.2-.22.42-.07.68'
                ' .5.87 1.3 1.67 2.2 2.2.26.15.48.12.68-.07l.42-.4c.18-.2.4-.24.66-.14l1.55.66c.37.16.5.36'
                '.5.66 0 1-.85 1.85-1.9 1.85-3.4 0-6.9-3.5-6.9-6.9 0-1.05.85-1.9 1.9-1.9z"/></svg>',
}
