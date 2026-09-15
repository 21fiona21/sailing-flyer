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

## Editing the copy

Everything visitors read is in `content.py`. Use `<strong>` to bold keywords in
a description. `info` renders the "Free for members" style field; add `hiring`
to a panel for a recruiting sticker on both faces.

## Adding or replacing photos

1. Drop the original in `images/` (originals are gitignored).
2. Crop to 9:16 and compress:

```bash
cd images
sips --resampleHeight 1280 yourphoto.jpg -o t.jpg
sips -c 1280 720 t.jpg -o c.jpg
sips -s format jpeg -s formatOptions 42 c.jpg -o <slug>.9x16.jpg
rm t.jpg c.jpg
```

3. Point a panel's `image` at `<slug>`.

Photos are **centre-cropped**, so check the subject is not cut off. They are
inlined as base64 because the component runs in a srcdoc iframe where relative
paths do not resolve — which is also why page weight matters: the whole flyer
is currently about 1 MB, loaded over mobile data at the fair.

## The logo

`icons.py` holds a placeholder sail. Replace `LOGO` with the club's SVG —
transparent background, single colour (white reads best over photos).

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
