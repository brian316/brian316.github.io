"""Generate initials favicons ("BD", Instrument Serif, paper on ink) into static/.

Run from the repo root:
    uv run --with pillow python scripts/make_favicon.py path/to/InstrumentSerif-Regular.ttf
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK = (11, 13, 11)
PAPER = (245, 244, 237)
ACCENT = (247, 89, 31)
TEXT = "BD"
MASTER = 512


def render(font_path: str, small: bool = False) -> Image.Image:
    """small=True: for 16-32px tabs. Bigger, slightly thickened letters and no accent bar,
    because Instrument Serif's hairlines vanish at that size."""
    img = Image.new("RGBA", (MASTER, MASTER), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, MASTER - 1, MASTER - 1), radius=int(MASTER * 0.16), fill=INK)
    font = ImageFont.truetype(font_path, int(MASTER * (0.80 if small else 0.62)))
    stroke = int(MASTER * 0.014) if small else 0
    l, t, r, b = d.textbbox((0, 0), TEXT, font=font, stroke_width=stroke)
    x = (MASTER - (r - l)) / 2 - l
    y = (MASTER - (b - t)) / 2 - t - (0 if small else MASTER * 0.03)
    d.text((x, y), TEXT, font=font, fill=PAPER, stroke_width=stroke, stroke_fill=PAPER)
    if small:
        return img
    # small accent bar under the initials
    bar_w, bar_h = MASTER * 0.30, MASTER * 0.035
    by = y + b + MASTER * 0.05
    d.rectangle(((MASTER - bar_w) / 2, by, (MASTER + bar_w) / 2, by + bar_h), fill=ACCENT)
    return img


def main(font_path: str, out_dir: Path = Path("static")) -> None:
    master = render(font_path)
    small = render(font_path, small=True)
    sized = lambda n: master.resize((n, n), Image.LANCZOS)
    tab = lambda n: small.resize((n, n), Image.LANCZOS)
    tab(48).save(out_dir / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                 append_images=[tab(16), tab(32)])
    tab(32).save(out_dir / "favicon-32.png")
    # iOS masks its own corners and dislikes transparency: flatten onto ink.
    touch = Image.new("RGB", (180, 180), INK)
    touch.paste(sized(180), (0, 0), sized(180))
    touch.save(out_dir / "apple-touch-icon.png")


if __name__ == "__main__":
    main(sys.argv[1])
