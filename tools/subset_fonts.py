"""Build the self-hosted fonts in fonts/ so the app works offline.

Downloads each font from Google's open-source font repository, trims variable fonts to the
weights the app uses, and keeps only the characters it needs:
  * Latin fonts: English, pinyin tone marks and common punctuation.
  * Noto Sans SC: exactly the Chinese characters that appear in index.html.

Run it again whenever new Chinese characters are added to index.html:
    pip install fonttools brotli
    python tools/subset_fonts.py

Downloads are cached in the system temp folder, not in the project.
"""
import os
import sys
import tempfile
import urllib.request

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "fonts")
CACHE = os.path.join(tempfile.gettempdir(), "lgp-font-cache")
BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

# Basic Latin, Latin-1, Latin Extended-A, pinyin with caron (ǎ ǐ ǒ ǔ ǖ ǘ ǚ ǜ), combining marks,
# general punctuation, multiplication sign and minus sign.
LATIN = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + list(range(0x1CD, 0x1DD))
    + list(range(0x300, 0x370)) + list(range(0x2010, 0x2060)) + [0x2212]
)

# (output file, source path, axis limits or None)
FONTS = [
    ("fredoka.woff2", "fredoka/Fredoka[wdth,wght].ttf", {"wght": (500, 700), "wdth": 100}),
    ("nunito.woff2", "nunito/Nunito[wght].ttf", {"wght": (400, 800)}),
    ("andika-regular.woff2", "andika/Andika-Regular.ttf", None),
    ("andika-bold.woff2", "andika/Andika-Bold.ttf", None),
    ("racing-sans-one.woff2", "racingsansone/RacingSansOne-Regular.ttf", None),
    ("noto-sans-sc.woff2", "notosanssc/NotoSansSC[wght].ttf", {"wght": (500, 700)}),
]


def chinese_chars():
    """Every CJK character and CJK punctuation mark used in index.html."""
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        text = f.read()
    keep = {
        ord(c) for c in text
        if 0x2E80 <= ord(c) <= 0x9FFF or 0xFF00 <= ord(c) <= 0xFFEF or 0x3000 <= ord(c) <= 0x303F
    }
    return sorted(keep) + list(range(0x20, 0x7F))


def fetch(path):
    os.makedirs(CACHE, exist_ok=True)
    local = os.path.join(CACHE, path.replace("/", "_"))
    if not os.path.exists(local):
        url = BASE + urllib.request.quote(path)
        print("downloading", url)
        urllib.request.urlretrieve(url, local)
    return local


def build(out_name, src, axes, unicodes):
    font = TTFont(fetch(src))
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.hinting = False
    opts.desubroutinize = True
    sub = Subsetter(opts)
    sub.populate(unicodes=unicodes)
    sub.subset(font)
    # Narrow the weight range after subsetting (doing it first trips a fontTools bug on gvar).
    if axes:
        font = instantiateVariableFont(font, axes)
    path = os.path.join(OUT, out_name)
    font.flavor = "woff2"
    font.save(path)
    print(f"{out_name}: {os.path.getsize(path) // 1024} KB")


def main():
    os.makedirs(OUT, exist_ok=True)
    zh = chinese_chars()
    print(f"Chinese characters found in index.html: {len(zh) - 95}")
    for out_name, src, axes in FONTS:
        build(out_name, src, axes, zh if out_name.startswith("noto") else LATIN)


if __name__ == "__main__":
    sys.exit(main())
