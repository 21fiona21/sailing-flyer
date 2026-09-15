"""Inline SVG icons. Inline so the flyer stays a single self-contained page."""

# Club logo placeholder: transparent, white, reads over a photo.
LOGO = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M52 6 L52 78 L90 78 Z" fill="#ffffff" opacity="0.95"/>
  <path d="M46 26 L46 78 L14 78 Z" fill="#ffffff" opacity="0.7"/>
  <path d="M6 84 q22 10 44 0 q22 -10 44 0 l0 8 q-22 -10 -44 0 q-22 10 -44 0 Z" fill="#ffffff" opacity="0.9"/>
</svg>
"""

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
