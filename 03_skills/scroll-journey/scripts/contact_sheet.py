#!/usr/bin/env python3
"""
CONTACT SHEET: sample a clip at a fixed interval and tile the frames into timecoded sheets that
an AI model (or a person) can read as still images. Claude sees stills, not motion, so this is
how a render is "watched": a 2 fps sheet of an 8 s passage shows every phase of the flight.

usage: python3 -B contact_sheet.py SOURCE OUTDIR SLUG [interval_seconds] [cols] [rows]
                                    [--offset SEC] [--window SEC] [--tile-width 440]
       python3 -B contact_sheet.py --selftest
interval_seconds may be fractional (0.5 = 2 frames per second). Writes OUTDIR/SLUG_sheetNN.jpg
and prints each path. Exit 0 / 1 (no frames) / 2 usage.
"""
import math
import os
import shutil
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def hms(t):
    t = int(round(t))
    return f"{t // 3600:d}:{(t % 3600) // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:d}:{t % 60:02d}"


def extract(src, workdir, interval, tile_w, offset=0.0, window=0.0):
    os.makedirs(workdir, exist_ok=True)
    for f in os.listdir(workdir):
        os.remove(os.path.join(workdir, f))
    # -fps_mode passthrough keeps one output frame per selected frame (no duplication or drop);
    # -ss BEFORE -i is an input seek, so the first output frame lands on `offset`
    args = []
    if offset:
        args += ["-ss", f"{offset:.3f}"]
    args += ["-i", V.need(src)]
    if window:
        args += ["-t", f"{window:.3f}"]
    args += ["-vf", f"fps=1/{interval},scale={tile_w}:-2", "-fps_mode", "passthrough",
             os.path.join(workdir, "f_%05d.jpg")]
    # a window past the clip's end writes nothing and ffmpeg exits non-zero: that is "no frames"
    V.ff(args, check=False)
    return sorted(os.listdir(workdir))


def build(src, outdir, slug, interval=15.0, cols=6, rows=5, tile_w=440, offset=0.0, window=0.0):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True)
    work = os.path.join(V.scratch_root(), f"contact_{os.getpid()}_{slug}")
    dur = V.probe(src)["duration"]
    try:
        frames = extract(src, work, interval, tile_w, offset, window)
        if not frames:
            return dur, []
        font = V.pil_font(26)
        tw, th = Image.open(os.path.join(work, frames[0])).size
        band = 34                                      # timecode strip under each tile
        per_sheet = cols * rows
        made = []
        for s in range(math.ceil(len(frames) / per_sheet)):
            chunk = frames[s * per_sheet:(s + 1) * per_sheet]
            sheet = Image.new("RGB", (cols * tw, math.ceil(len(chunk) / cols) * (th + band)),
                              (16, 16, 18))
            draw = ImageDraw.Draw(sheet)
            for i, fn in enumerate(chunk):
                t = offset + (s * per_sheet + i) * interval
                x, y = (i % cols) * tw, (i // cols) * (th + band)
                sheet.paste(Image.open(os.path.join(work, fn)), (x, y))
                draw.rectangle([x, y + th, x + tw, y + th + band], fill=(200, 60, 20))
                label = hms(t) if interval >= 1 else f"{t:.2f}s"
                draw.text((x + 8, y + th + 4), label, font=font, fill=(255, 255, 255))
            out = os.path.join(outdir, f"{slug}_sheet{s + 1:02d}.jpg")
            sheet.save(out, quality=82, optimize=True)
            made.append(out)
        return dur, made
    finally:
        shutil.rmtree(work, ignore_errors=True)


def selftest():
    d = V.selftest_dir("contact_sheet")
    try:
        from PIL import Image
        clip = V.lavfi_clip(os.path.join(d, "clip.mp4"), duration=4.0)
        # 2 fps over 4 s = 8 frames, 4 x 2 per sheet -> exactly one sheet of 4 x 2 tiles
        dur, made = build(clip, d, "t", interval=0.5, cols=4, rows=2, tile_w=160)
        size = Image.open(made[0]).size if made else (0, 0)
        t_one = len(made) == 1 and size == (4 * 160, 2 * (90 + 34))
        # a smaller sheet forces a second sheet: 8 frames at 3 per sheet -> 3 sheets
        _, made3 = build(clip, d, "u", interval=0.5, cols=3, rows=1, tile_w=160)
        t_three = len(made3) == 3
        # positive control: a window past the end of the clip yields no frames and no sheet
        _, none = build(clip, d, "v", interval=0.5, cols=4, rows=2, tile_w=160, offset=10.0)
        t_control = none == []
        ok = t_one and t_three and t_control
        print(f"selftest contact_sheet: duration={dur:.2f}s sheets={len(made)} size={size[0]}x{size[1]} "
              f"| three_sheets={int(t_three)} | control_past_end_sheets={len(none)} "
              f"-> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?"); ap.add_argument("outdir", nargs="?")
    ap.add_argument("slug", nargs="?")
    ap.add_argument("interval", nargs="?", type=float, default=15.0,
                    help="seconds between samples; fractional is allowed (0.5 = 2 per second)")
    ap.add_argument("cols", nargs="?", type=int, default=6)
    ap.add_argument("rows", nargs="?", type=int, default=5)
    ap.add_argument("--offset", type=float, default=0.0, help="start sampling at this second")
    ap.add_argument("--window", type=float, default=0.0,
                    help="only sample this many seconds from --offset (0 = to the end)")
    ap.add_argument("--tile-width", type=int, default=440)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.src or not a.outdir or not a.slug:
        ap.print_usage(sys.stderr); return 2
    if a.interval <= 0:
        raise V.ToolError("interval must be above 0")
    dur, made = build(a.src, a.outdir, a.slug, a.interval, a.cols, a.rows, a.tile_width,
                      a.offset, a.window)
    if not made:
        print(f"NO FRAMES for {a.slug}", file=sys.stderr)
        return 1
    print(f"{a.slug}: duration={hms(dur)} sheets={len(made)} interval={a.interval}s")
    for m in made:
        print(f"  {m}  ({os.path.getsize(m) // 1024} KB)")
    return 0


if __name__ == "__main__":
    V.main_guard(main)
