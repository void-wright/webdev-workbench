#!/usr/bin/env python3
"""
PLACEHOLDER STILLS: paint labelled stand-in stops so the Astro template builds and can be laid
out before the real paintings exist. Never ship these: replace every file with the real stop.

For each stop i it writes OUTDIR/s{i}-w.jpg (wide, 1376 x 768) and OUTDIR/s{i}-p.jpg (phone,
768 x 1376). The form is a soft blob on the side AWAY from the words (sides alternate, starting
with the words on the left, as the example data does); on phones the form sits in the top third,
leaving the lower part calm for the words. --theme light paints on #FFFFFF with clean white
edges; --theme dark paints a night ground.

usage: python3 -B placeholder_stills.py OUTDIR --stops 4 --theme light|dark [--sides l,r,l,c]
       python3 -B placeholder_stills.py --selftest
Prints each path written. Exit 0 / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

WIDE, PHONE = (1376, 768), (768, 1376)
THEMES = {
    # ground, blob colours (cycled), label colour
    "light": ((255, 255, 255), [(92, 140, 96), (196, 150, 70), (90, 120, 170), (170, 100, 90)], (120, 120, 120)),
    "dark": ((14, 18, 30), [(70, 110, 190), (150, 90, 170), (60, 150, 150), (190, 150, 80)], (150, 160, 180)),
}


def paint(size, ground, colour, box, label, label_colour, blur):
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.new("RGB", size, ground)
    ImageDraw.Draw(im).ellipse(box, fill=colour)
    im = im.filter(ImageFilter.GaussianBlur(blur))
    ImageDraw.Draw(im).text((24, 24) if size[0] > size[1] else (24, size[1] // 2),
                            label, font=V.pil_font(28), fill=label_colour)
    return im


def make(outdir, stops=4, theme="light", sides=None):
    if stops < 2:
        raise V.ToolError("--stops must be 2 or more")
    if theme not in THEMES:
        raise V.ToolError("--theme must be light or dark")
    sides = sides or [("l", "r")[i % 2] for i in range(stops)]
    if len(sides) != stops or any(s not in ("l", "r", "c") for s in sides):
        raise V.ToolError("--sides needs one of l, r, c per stop")
    ground, colours, lc = THEMES[theme]
    os.makedirs(outdir, exist_ok=True)
    out = []
    W, H = WIDE
    for i in range(stops):
        col = colours[i % len(colours)]
        # wide: the form on the side away from the words (centre stops: the form low and wide)
        box = {"l": (int(W * 0.55), int(H * 0.2), int(W * 0.92), int(H * 0.8)),
               "r": (int(W * 0.08), int(H * 0.2), int(W * 0.45), int(H * 0.8)),
               "c": (int(W * 0.25), int(H * 0.62), int(W * 0.75), int(H * 0.88))}[sides[i]]
        pw = os.path.join(outdir, f"s{i}-w.jpg")
        paint(WIDE, ground, col, box, f"PLACEHOLDER S{i} wide", lc, 40).save(pw, quality=88)
        # phone: the form in the top third, the lower part calm for the words
        pw2 = os.path.join(outdir, f"s{i}-p.jpg")
        pbox = (int(PHONE[0] * 0.18), int(PHONE[1] * 0.08), int(PHONE[0] * 0.82), int(PHONE[1] * 0.36))
        paint(PHONE, ground, col, pbox, f"PLACEHOLDER S{i} phone", lc, 36).save(pw2, quality=88)
        out += [pw, pw2]
    return out


def selftest():
    d = V.selftest_dir("placeholder_stills")
    try:
        from PIL import Image
        import stop_check as SC
        files = make(d, 3, "light")
        t_count = len(files) == 6 and all(os.path.isfile(f) for f in files)
        t_dims = Image.open(files[0]).size == WIDE and Image.open(files[1]).size == PHONE
        # the words side of each wide still is calm and the edges are white paper
        r0 = SC.check(files[0], "left", "light", paper=True)
        r1 = SC.check(files[2], "right", "light", paper=True)
        rp = SC.check(files[1], "bottom", "light", paper=True)
        # positive control: the form's side must be flagged
        rc = SC.check(files[0], "right", "light")
        ok = (t_count and t_dims and r0["verdict"] == "PASS" and r1["verdict"] == "PASS"
              and rp["verdict"] == "PASS" and rc["verdict"] == "FLAG")
        print(f"selftest placeholder_stills: files={len(files)} dims_ok={int(t_dims)} "
              f"s0_left={r0['verdict']} s1_right={r1['verdict']} s0_phone_bottom={rp['verdict']} "
              f"| control_form_side={rc['verdict']} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--stops", type=int, default=4)
    ap.add_argument("--theme", default="light")
    ap.add_argument("--sides", help="comma list of l, r or c per stop (where the WORDS sit)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.outdir:
        ap.print_usage(sys.stderr); return 2
    sides = [x.strip() for x in a.sides.split(",")] if a.sides else None
    for f in make(a.outdir, a.stops, a.theme, sides):
        print(f)
    return 0


if __name__ == "__main__":
    V.main_guard(main)
