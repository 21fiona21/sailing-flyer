# HSG Sailing — digital flyer

Mobile-first, snap-scrolling one-pager. Visitors reach it by scanning a QR code
at the club fair.

## Run it locally

```bash
cd ~/sailing-flyer
.venv/bin/streamlit run app.py
```

Then open the Network URL on your phone. If it will not connect, get the
current IP with `ipconfig getifaddr en0` — your router can reassign it.

Deployed on Streamlit Community Cloud from `main`; pushing redeploys.

## Files

| File | What's in it |
|---|---|
| `content.py` | **All the copy.** Titles, captions, descriptions, info lines, links. |
| `render.py` | Turns the content into HTML. Four panel types: hero, flip, list, contact. |
| `icons.py` | Inline SVG logo and icons. |
| `app.py` | Page shell: CSS, the sizing JS, and the Streamlit chrome overrides. |
| `images/` | Photos, cropped to 9:16. Only the `.9x16.jpg` versions are committed. |
| `assets/` | Club logo, white on transparency: `logo-mark.png` (roundel) and `logo-full.png` (with wordmark). |

## Editing the copy

Everything visitors read is in `content.py`. Use `<strong>` to bold keywords in
a description. `info` renders the "Free for members" style field; add `hiring`
to a panel for a recruiting sticker on both faces.

## Adding or replacing photos

1. Drop the full-size original in `images/originals/` (gitignored).
2. Crop and compress with Pillow — **not `sips`**, which ignores EXIF rotation
   and silently turns portrait phone photos sideways:

```python
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open("images/originals/x.jpg")).convert("RGB")
out = ImageOps.fit(im, (720, 1280), method=Image.LANCZOS, centering=(0.5, 0.5))
out.save("images/<slug>.9x16.jpg", "JPEG", quality=62, optimize=True, progressive=True)
```

3. Point a panel's `image` at `<slug>`. Omit `image` entirely and the panel
   gets a gradient built from its `color` instead.

Photos are **centre-cropped**, so check the subject survives. They are inlined
as base64 because the component runs in a srcdoc iframe where relative paths do
not resolve — which is also why page weight matters: the whole flyer is about
1 MB, loaded over mobile data at the fair.

Each panel's dark overlay is **computed from the photo**: `render.py` measures
the brightness of the band where the headline sits and scales the scrim to
match, so a bright sky gets more darkening than a dusk shot. Drop in a new
photo and the contrast looks after itself.

## The logo

`assets/logo-mark.png` (roundel) and `assets/logo-full.png` (roundel plus
"HSG SAILING" wordmark), both white on transparency. The hero uses the mark,
because the panel already says "HSG Sailing" in text; the contact page uses the
full lockup.

These were rebuilt from the club's SVG, which wrapped a raster whose alpha came
from luminance — that made the background opaque and knocked out the artwork, so
it rendered as a white box. If a new logo is supplied, check it over a photo
before trusting it.

## Gotchas worth knowing

- **Panel height** is set by JavaScript from the real window height, not CSS
  alone. `100dvh` inside an iframe measures the iframe, which once made every
  panel 900px tall and clipped the bottom on phones.
- **The inactive card face** is hidden with `visibility`, not just
  `backface-visibility` — Safari leaks text-shadowed children through an
  otherwise hidden face, which showed the front title mirrored on the back.
- **No Streamlit widgets.** A widget interaction reruns the script and would
  reset the visitor's scroll position.
- **Links must use `target="_blank"`.** The component iframe is sandboxed
  without `allow-top-navigation`, so same-tab navigation is blocked.
- **Community Cloud apps sleep** after about a week idle and show a slow wake-up
  screen. Open the URL shortly before the fair.

Placeholder photo licences: see `images/CREDITS.md`.
