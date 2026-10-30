#!/usr/bin/env python3
"""
STOP CHECK: is a painted stop ready to carry words and to meet a passage?

Measures one still (no video, CPU only):
  words area   the region where the HTML copy will sit (--side), as luminance statistics:
               mean, p5, p95 and standard deviation (busyness). Wide stills: left or right
               40 % column (or the centre's upper sky); portrait stills: the lower 45 %.
  contrast     WCAG contrast of --text (the copy colour) against the WORST 5 % of the words
               area: its brightest 5 % for light text on a dark theme, its darkest 5 % for dark
               text on a light theme. This is the contrast before any veil, so it shows how much
               veil the page will need.
  paper        (--paper, white-page journeys) the 4 % bands at the top and bottom edges must be
               the page's white: p5 luminance >= --paper-min (default 248).

Bands are STARTING GUESSES, not measured thresholds for your art: words area busyness
(std) <= 28, raw contrast >= 3.0 (the page's veil then lifts it to 4.5 or more). Judge the
numbers next to the picture, never instead of it.

usage: python3 -B stop_check.py STILL --side left|right|center|bottom --theme dark|light
                                 [--text #RRGGBB] [--paper] [--min-contrast 3.0] [--max-std 28]
       python3 -B stop_check.py --selftest
JSON report on stdout. Exit 0 all checks pass / 1 any check flagged / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

DEFAULT_TEXT = {"dark": "#F2EDE4", "light": "#1C1F24"}


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) != 6:
        raise V.ToolError(f"bad colour {h!r}, want #RRGGBB")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_lum_from_rgb(rgb):
    """WCAG relative luminance from 0-255 sRGB (array or tuple, last axis RGB)."""
    import numpy as np
    c = np.asarray(rgb, dtype="float64") / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def region(h, w, side, portrait):
    """(y0, y1, x0, x1) of the words area, in pixels."""
    if portrait or side == "bottom":
        return int(h * 0.55), h, 0, w
    if side == "left":
        return int(h * 0.15), int(h * 0.85), 0, int(w * 0.40)
    if side == "right":
        return int(h * 0.15), int(h * 0.85), int(w * 0.60), w
    if side == "center":
        return int(h * 0.15), int(h * 0.60), int(w * 0.25), int(w * 0.75)
    raise V.ToolError(f"bad --side {side!r}")


def check(still, side, theme, text=None, paper=False, paper_min=248.0, min_contrast=3.0,
          max_std=28.0):
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(V.need(still)).convert("RGB")).astype("float64")
    h, w, _ = im.shape
    portrait = h > w
    y0, y1, x0, x1 = region(h, w, side, portrait)
    area = im[y0:y1, x0:x1].reshape(-1, 3)
    luma = area[:, 0] * 0.2126 + area[:, 1] * 0.7152 + area[:, 2] * 0.0722
    rl = rel_lum_from_rgb(area)
    worst = np.percentile(rl, 95) if theme == "dark" else np.percentile(rl, 5)
    tl = float(rel_lum_from_rgb(hex_rgb(text or DEFAULT_TEXT[theme])))
    cr = contrast(tl, float(worst))
    rep = {"still": still, "size": f"{w}x{h}", "portrait": portrait, "side": side,
           "theme": theme, "words_area": [x0, y0, x1, y1],
           "luma_mean": round(float(luma.mean()), 1), "luma_p5": round(float(np.percentile(luma, 5)), 1),
           "luma_p95": round(float(np.percentile(luma, 95)), 1), "luma_std": round(float(luma.std()), 1),
           "text": text or DEFAULT_TEXT[theme], "raw_contrast_worst5": round(cr, 2)}
    flags = []
    if rep["luma_std"] > max_std:
        flags.append(f"busy_words_area_std>{max_std}")
    if cr < min_contrast:
        flags.append(f"raw_contrast<{min_contrast}")
    if paper:
        band = max(1, int(h * 0.04))
        def p5(a):
            L = a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722
            return float(np.percentile(L, 5))
        rep["paper_top_p5"] = round(p5(im[:band]), 1)
        rep["paper_bottom_p5"] = round(p5(im[-band:]), 1)
        if min(rep["paper_top_p5"], rep["paper_bottom_p5"]) < paper_min:
            flags.append(f"paper_edge<{paper_min}")
    rep["flags"] = flags
    rep["verdict"] = "FLAG" if flags else "PASS"
    return rep


def selftest():
    d = V.selftest_dir("stop_check")
    try:
        from PIL import Image, ImageDraw, ImageFilter
        # a white-paper still: a dark-green pigment blob on the RIGHT, calm paper on the left
        im = Image.new("RGB", (1376, 768), (255, 255, 255))
        ImageDraw.Draw(im).ellipse([860, 180, 1260, 600], fill=(46, 90, 60))
        im = im.filter(ImageFilter.GaussianBlur(30))
        light = os.path.join(d, "light.png"); im.save(light)
        good = check(light, "left", "light", paper=True)
        # positive control 1: words on the pigment side must be flagged
        bad = check(light, "right", "light", paper=True)
        # positive control 2: a grey paper edge must be flagged
        grey = Image.new("RGB", (1376, 768), (236, 236, 236))
        gp = os.path.join(d, "grey.png"); grey.save(gp)
        gpr = check(gp, "left", "light", paper=True)
        # a night-sky still: bright stars on the left, calm dark sky on the right
        sky = Image.new("RGB", (1376, 768), (14, 18, 30))
        dr = ImageDraw.Draw(sky)
        for k in range(400):
            x, y = (k * 97) % 520, (k * 61) % 768
            dr.ellipse([x, y, x + 6, y + 6], fill=(250, 250, 255))
        sp = os.path.join(d, "sky.png"); sky.save(sp)
        dgood = check(sp, "right", "dark")
        dbad = check(sp, "left", "dark")
        ok = (good["verdict"] == "PASS" and bad["verdict"] == "FLAG" and
              any(f.startswith("paper_edge") for f in gpr["flags"]) and
              dgood["verdict"] == "PASS" and dbad["verdict"] == "FLAG")
        print(f"selftest stop_check: light_left={good['verdict']} contrast={good['raw_contrast_worst5']} "
              f"| control_light_right={bad['verdict']} {bad['flags']} | control_grey_paper="
              f"{gpr['flags']} | dark_right={dgood['verdict']} contrast={dgood['raw_contrast_worst5']} "
              f"| control_dark_left={dbad['verdict']} {dbad['flags']} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("still", nargs="?")
    ap.add_argument("--side", choices=["left", "right", "center", "bottom"])
    ap.add_argument("--theme", choices=["dark", "light"])
    ap.add_argument("--text", help="the copy colour, #RRGGBB (default: #F2EDE4 dark, #1C1F24 light)")
    ap.add_argument("--paper", action="store_true", help="white-page journey: judge the edge bands")
    ap.add_argument("--paper-min", type=float, default=248.0)
    ap.add_argument("--min-contrast", type=float, default=3.0)
    ap.add_argument("--max-std", type=float, default=28.0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.still or not a.side or not a.theme:
        ap.print_usage(sys.stderr); return 2
    rep = check(a.still, a.side, a.theme, a.text, a.paper, a.paper_min, a.min_contrast, a.max_std)
    V.emit(rep)
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    V.main_guard(main)
