#!/usr/bin/env python3
"""
ROUTE SHEET: one contact sheet of a whole scroll route, in route order, for the seam review.

One row per passage:   [ stop i | passage first | passage mid | passage last | stop i+1 ]
The two seam pairs (stop i | first, last | stop i+1) sit side by side. Each tile carries a
drawtext label with its timestamp and frame index; each seam pair's divider is GREEN when the
measured seam SSIM >= --min-ssim and RED when it is not, with the SSIM printed in the label.

usage: python3 -B route_sheet.py --stops S0.png S1.png ... --passages P1.mp4 P2.mp4 ... OUT.jpg
                                 [--tile-width 360] [--min-ssim 0.90]
       python3 -B route_sheet.py --selftest
Needs exactly one more stop than passages. Prints the sheet path, size, and per-seam SSIMs.
Exit 0 all seams >= --min-ssim / 1 any seam below / 2 usage (incl. count mismatch).
"""
import os
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

BAND = 30
GUT = 8
GREEN, RED, DARK = (40, 170, 90), (210, 50, 40), (16, 16, 18)


def tile(src, out, tw, th, label, td, select=None, last=False):
    """Scale-to-cover one frame (or still) into tw x th, then add a label band under it.
    The label is drawn with Pillow (no ffmpeg drawtext, so no freetype or font path needed)."""
    from PIL import Image, ImageDraw
    vf = V.cover_filter(tw, th)
    if last:
        src = V.last_frame(src, os.path.join(td, os.path.basename(out) + ".last.png"))
    elif select is not None:
        vf = r"select=eq(n\," + str(int(select)) + ")," + vf
    raw = os.path.join(td, os.path.basename(out) + ".raw.png")
    V.ff(["-i", src, "-vf", vf, "-frames:v", "1", raw])
    im = Image.new("RGB", (tw, th + BAND), (16, 16, 18))
    im.paste(Image.open(raw).convert("RGB"), (0, 0))
    ImageDraw.Draw(im).text((8, th + 7), label, font=V.pil_font(16), fill=(255, 255, 255))
    im.save(out)
    return out


def build(stops, passages, out, tw=360, min_ssim=0.90):
    if len(stops) != len(passages) + 1:
        raise V.ToolError(f"need len(stops) == len(passages)+1, got {len(stops)} and "
                          f"{len(passages)}")
    for p in stops + passages:
        V.need(p)
    from PIL import Image, ImageDraw
    i0 = V.probe(passages[0])
    th = int(round(tw * i0["height"] / i0["width"] / 2)) * 2
    seams = []
    rows = []
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        for k, p in enumerate(passages):
            info = V.probe(p)
            n, fps = info["frames"], info["fps"]
            mid = n // 2
            ff_ = V.first_frame(p, os.path.join(td, f"p{k}_f.png"))
            fl_ = V.last_frame(p, os.path.join(td, f"p{k}_l.png"))
            s_in = V.ssim_images(ff_, stops[k], info["width"], info["height"])
            s_out = V.ssim_images(fl_, stops[k + 1], info["width"], info["height"])
            seams.append((f"S{k}>P{k + 1}", s_in)); seams.append((f"P{k + 1}>S{k + 1}", s_out))
            pn = f"P{k + 1}"
            t = [
                tile(stops[k], os.path.join(td, f"r{k}_0.png"), tw, th, f"S{k} stop", td),
                tile(p, os.path.join(td, f"r{k}_1.png"), tw, th,
                     f"{pn} first 0.000s n0  seam {s_in:.3f}", td, select=0),
                tile(p, os.path.join(td, f"r{k}_2.png"), tw, th,
                     f"{pn} mid {mid / fps:.3f}s n{mid}", td, select=mid),
                tile(p, os.path.join(td, f"r{k}_3.png"), tw, th,
                     f"{pn} last {(n - 1) / fps:.3f}s n{n - 1}  seam {s_out:.3f}", td, last=True),
                tile(stops[k + 1], os.path.join(td, f"r{k}_4.png"), tw, th, f"S{k + 1} stop", td),
            ]
            rows.append(([Image.open(x).convert("RGB") for x in t], s_in, s_out))
        W = 5 * tw + 4 * GUT
        H = len(rows) * (th + BAND) + (len(rows) - 1) * GUT
        sheet = Image.new("RGB", (W, H), DARK)
        draw = ImageDraw.Draw(sheet)
        for r, (ims, s_in, s_out) in enumerate(rows):
            y = r * (th + BAND + GUT)
            for c, im in enumerate(ims):
                sheet.paste(im, (c * (tw + GUT), y))
            for c, s in ((0, s_in), (3, s_out)):      # gutters after tile 0 and tile 3 = seams
                x = c * (tw + GUT) + tw
                draw.rectangle([x, y, x + GUT - 1, y + th + BAND - 1],
                               fill=GREEN if s >= min_ssim else RED)
        os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
        sheet.save(out, quality=86, optimize=True)
    return {"out": out, "size": sheet.size, "seams": seams,
            "below": [n for n, s in seams if s < min_ssim]}


def selftest():
    d = V.selftest_dir("route_sheet")
    try:
        HUE = "hue=H=n*0.05"
        s0 = V.lavfi_still(os.path.join(d, "s0.png"), t=0, extra_vf=HUE)
        s1 = V.lavfi_still(os.path.join(d, "s1.png"), t=47 / 24, extra_vf=HUE)
        # two passages cut from ONE continuous take, sharing frame 47 (= stop S1)
        take = V.lavfi_clip(os.path.join(d, "take.mp4"), duration=4.0, crf=14, extra_vf=HUE)
        p1, p2 = os.path.join(d, "p1.mp4"), os.path.join(d, "p2.mp4")
        for o, tr in ((p1, "trim=end_frame=48"), (p2, "trim=start_frame=47")):
            V.ff(["-i", take, "-vf", f"{tr},setpts=PTS-STARTPTS", "-c:v", "libx264",
                  "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", o])
        # positive control: passage 2's END stop is a WRONG image
        wrong = V.lavfi_still(os.path.join(d, "wrong.png"), src="smptehdbars")
        out = os.path.join(d, "route.jpg")
        r = build([s0, s1, wrong], [p1, p2], out, tw=240)
        exp = (5 * 240 + 4 * GUT, 2 * (136 + BAND) + GUT)
        t_size = tuple(r["size"]) == exp and os.path.isfile(out)
        t_good = [n for n, _ in r["seams"][:3]] == ["S0>P1", "P1>S1", "S1>P2"] and \
            all(s >= 0.9 for _, s in r["seams"][:3])
        t_control = r["below"] == ["P2>S2"]
        # positive control 2: a stop/passage count mismatch must be refused (exit 2 path)
        try:
            build([s0, s1], [p1, p2], out); t_count = False
        except V.ToolError:
            t_count = True
        ok = t_size and t_good and t_control and t_count
        print(f"selftest route_sheet: size={r['size'][0]}x{r['size'][1]} "
              f"seams={[round(s, 3) for _, s in r['seams']]} | control_wrong_stop_flagged="
              f"{'FAIL' if t_control else 'missed'} control_count_mismatch="
              f"{'REFUSED' if t_count else 'accepted'} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", nargs="?")
    ap.add_argument("--stops", nargs="+", default=[])
    ap.add_argument("--passages", nargs="+", default=[])
    ap.add_argument("--tile-width", type=int, default=360)
    ap.add_argument("--min-ssim", type=float, default=0.90)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    # `--passages P1 P2 OUT.jpg` lets nargs="+" swallow the output path: take it back
    if not a.out and a.passages and a.passages[-1].lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        a.out = a.passages.pop()
    if not a.out or not a.stops or not a.passages:
        ap.print_usage(sys.stderr); return 2
    r = build(a.stops, a.passages, a.out, a.tile_width, a.min_ssim)
    print(f"{r['out']}  {r['size'][0]}x{r['size'][1]}  bytes={os.path.getsize(r['out'])}")
    for n, s in r["seams"]:
        print(f"{n} {s:.4f}")
    print(f"seams={len(r['seams'])} below_{a.min_ssim}={len(r['below'])}")
    return 1 if r["below"] else 0


if __name__ == "__main__":
    V.main_guard(main)
