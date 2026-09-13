# Digital flyer — university sailing club

Mobile-first, snap-scrolling one-pager built with Streamlit.

## Run it

```bash
cd ~/sailing-flyer
.venv/bin/streamlit run app.py
```

Open on your phone (same wifi): http://192.168.1.180:8501

## Edit the content

All text lives in the `PANELS` list at the top of `app.py`. Add, remove or
reorder entries — the progress dots on the right adjust automatically.

## Swap the coloured boxes for photos

1. Put your images in `~/sailing-flyer/images/`, cropped to 9:16.
2. In `PANELS`, replace `"color": "#1b6ca8"` with `"image": "beginners.jpg"`.
3. In `build_panel`, change the `style` to use the image, e.g.

```python
bg = f"url('data:image/jpeg;base64,{b64}')" if p.get("image") else p["color"]
```

(The component runs in a sandboxed iframe, so image files have to be inlined as
base64 rather than linked by path.)

The dark `.scrim` overlay on each panel is what keeps the text readable over a
busy photo — adjust the opacity values there rather than editing the photos.

## Logo

The placeholder sail is the inline `LOGO` SVG in `app.py`. Drop in your club's
SVG (transparent background, white fill) in its place.
