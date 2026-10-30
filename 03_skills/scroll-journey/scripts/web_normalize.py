#!/usr/bin/env python3
"""
WEB NORMALISE one passage clip for scroll scrubbing (the upstream sn-motion-html recipe):
cover-scale + crop to a fixed canvas, constant fps, libx264 yuv420p, a short FIXED GOP with
no scene-cut keyframes (-g N -keyint_min N -sc_threshold 0) so seeking is cheap both ways,
no audio (-an), +faststart (moov before mdat). Optional VP9 (.webm) and AV1 (.av1.mp4) twins.

A generator's export is an input, never the web asset. Fails (exit 1) if any written file is over
the --max-mb budget (decimal MB: 6 = 6,000,000 bytes); the file is kept so it can be inspected.

usage: python3 -B web_normalize.py CLIP OUT.mp4 [--trim START END]
         [--width 1280 --height 720 | --aspect 9:16 [--short-side 720]] [--crop-y 0..1]
         [--fps 24] [--gop 8 | --all-intra] [--crf 22] [--duration SEC] [--max-mb 6]
         [--webm] [--av1]
       python3 -B web_normalize.py --selftest
Prints one line per written file: path, bytes, frames, duration. Exit 0 / 1 / 2.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def dims(width=1280, height=720, aspect=None, short_side=720):
    if not aspect:
        return int(width) // 2 * 2, int(height) // 2 * 2
    try:
        aw, ah = (float(x) for x in aspect.split(":"))
    except ValueError:
        raise V.ToolError(f"bad --aspect {aspect!r}, want W:H")
    if aw >= ah:
        h = short_side; w = short_side * aw / ah
    else:
        w = short_side; h = short_side * ah / aw
    return int(round(w / 2)) * 2, int(round(h / 2)) * 2


def build_vf(w, h, fps, trim=None, crop_y=None, duration=None):
    parts = []
    if trim:
        parts.append(f"trim=start={float(trim[0]):.4f}:end={float(trim[1]):.4f},setpts=PTS-STARTPTS")
    parts += [V.cover_filter(w, h, crop_y), f"fps={fps}"]
    if duration:
        # exact duration: clone the last frame to pad a short clip, then cut
        parts.append(f"tpad=stop_mode=clone:stop_duration={float(duration):.4f},"
                     f"trim=duration={float(duration):.4f},setpts=PTS-STARTPTS")
    # limited (tv) range: JPEG-sourced clips arrive as full-range yuvj420p, which browsers and
    # verify_web_media reject; convert the range, then the format (a clip made from a still can arrive this way)
    parts.append("scale=out_range=tv,format=yuv420p")
    return ",".join(parts)


def normalize(src, out, trim=None, width=1280, height=720, aspect=None, short_side=720,
              crop_y=None, fps=24, gop=8, all_intra=False, crf=22, duration=None, max_mb=6.0,
              webm=False, av1=False, preset="slow"):
    """Returns (ok, [ {path, bytes, frames, duration, over_budget}, ... ])."""
    V.need(src)
    if trim and float(trim[1]) <= float(trim[0]):
        raise V.ToolError("--trim END must be after START")
    if webm and not V.has_encoder("libvpx-vp9"):
        raise V.ToolError("--webm needs an ffmpeg built with libvpx-vp9 (see `ffmpeg -encoders`)")
    if av1 and not V.has_encoder("libsvtav1"):
        raise V.ToolError("--av1 needs an ffmpeg built with libsvtav1 (see `ffmpeg -encoders`)")
    w, h = dims(width, height, aspect, short_side)
    g = 1 if all_intra else int(gop)
    vf = build_vf(w, h, fps, trim, crop_y, duration)
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    base = ["-i", src, "-an", "-sn", "-dn", "-map_metadata", "-1", "-vf", vf]
    V.ff(base + ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", "-color_range", "tv",
                 "-profile:v", "high", "-g", str(g), "-keyint_min", str(g), "-sc_threshold", "0",
                 "-x264-params", f"keyint={g}:min-keyint={g}:scenecut=0",
                 "-movflags", "+faststart", out])
    outs = [out]
    stem = os.path.splitext(out)[0]
    if webm:
        o = stem + ".webm"
        V.ff(base + ["-c:v", "libvpx-vp9", "-b:v", "0", "-crf", str(min(63, int(crf) + 12)),
                     "-row-mt", "1", "-deadline", "good", "-cpu-used", "2",
                     "-g", str(g), "-keyint_min", str(g), "-pix_fmt", "yuv420p", o])
        outs.append(o)
    if av1:
        o = stem + ".av1.mp4"
        V.ff(base + ["-c:v", "libsvtav1", "-crf", str(min(63, int(crf) + 12)), "-preset", "8",
                     "-g", str(g), "-svtav1-params", "scd=0", "-pix_fmt", "yuv420p",
                     "-movflags", "+faststart", o])
        outs.append(o)
    res, ok = [], True
    for o in outs:
        i = V.probe(o)
        over = i["bytes"] > max_mb * V.MB
        ok = ok and not over
        res.append({"path": o, "bytes": i["bytes"], "frames": i["frames"],
                    "duration": round(i["duration"], 3), "width": i["width"],
                    "height": i["height"], "over_budget": over})
    return ok, res


def selftest():
    d = V.selftest_dir("web_normalize")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import verify_web_media as VWM
        src = V.lavfi_clip(os.path.join(d, "raw.mp4"), size="1000x700", duration=4.0, audio=True)
        out = os.path.join(d, "web.mp4")
        # twins only where this ffmpeg has the encoder (reported as skipped otherwise)
        use_webm, use_av1 = V.has_encoder("libvpx-vp9"), V.has_encoder("libsvtav1")
        ok1, r1 = normalize(src, out, trim=(0.5, 3.5), fps=24, gop=8, webm=use_webm, av1=use_av1)
        v = VWM.verify(out, max_mb=6, expect_fps=24, expect_gop=8)
        t_dims = r1[0]["width"] == 1280 and r1[0]["height"] == 720 and r1[0]["frames"] == 72
        tv = [VWM.verify(x["path"], max_mb=6, expect_fps=24, expect_gop=8) for x in r1[1:]]
        t_twins = len(r1) == 1 + int(use_webm) + int(use_av1) and all(x["verdict"] == "PASS" for x in tv)
        # portrait + all-intra + exact duration (pads a 1 s clip to 2 s)
        out2 = os.path.join(d, "web_9x16.mp4")
        ok2, r2 = normalize(src, out2, trim=(0, 1), aspect="9:16", all_intra=True, duration=2.0)
        v2 = VWM.verify(out2, max_mb=6, expect_fps=24, expect_gop=1)
        t_port = r2[0]["width"] == 720 and r2[0]["height"] == 1280 and r2[0]["frames"] == 48
        # a JPEG-sourced (full-range yuvj420p) clip must come out limited-range yuv420p
        jpg = os.path.join(d, "still.jpg")
        V.ff(["-f", "lavfi", "-i", "testsrc2=size=640x360:rate=1", "-frames:v", "1", jpg])
        jsrc = os.path.join(d, "jpeg_src.mp4")
        V.ff(["-loop", "1", "-t", "1", "-i", jpg, "-c:v", "libx264", "-pix_fmt", "yuvj420p", jsrc])
        out3 = os.path.join(d, "web_jpeg.mp4")
        ok3, _ = normalize(jsrc, out3, fps=24, gop=8)
        v3 = VWM.verify(out3, max_mb=6, expect_fps=24, expect_gop=8)
        t_jpeg = ok3 and v3["verdict"] == "PASS"
        # positive control: an impossible budget must FAIL
        okc, _ = normalize(src, os.path.join(d, "tiny.mp4"), max_mb=0.001)
        good = ok1 and t_dims and t_twins and v["verdict"] == "PASS" and ok2 and t_port \
            and v2["verdict"] == "PASS" and t_jpeg and not okc
        print(f"selftest web_normalize: 16x9 {r1[0]['width']}x{r1[0]['height']} "
              f"frames={r1[0]['frames']} bytes={r1[0]['bytes']} verify={v['verdict']} "
              f"twins_verified={sum(x['verdict'] == 'PASS' for x in tv)}/{len(tv)} "
              f"twin_gops={[x['gop_max'] for x in tv]} webm={'yes' if use_webm else 'skipped'} "
              f"av1={'yes' if use_av1 else 'skipped'} | "
              f"9x16 {r2[0]['width']}x{r2[0]['height']} frames={r2[0]['frames']} "
              f"all_intra_verify={v2['verdict']} | jpeg_source_verify={v3['verdict']} | control_budget_0.001MB="
              f"{'FAIL' if not okc else 'PASS'} -> {'PASS' if good else 'FAIL'}")
        return 0 if good else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?"); ap.add_argument("out", nargs="?")
    ap.add_argument("--trim", nargs=2, type=float, metavar=("START", "END"),
                    help="source seconds to keep (frame-accurate trim filter)")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--aspect", help="e.g. 9:16 or 16:9; overrides --width/--height")
    ap.add_argument("--short-side", type=int, default=720, help="short side when --aspect is used")
    ap.add_argument("--crop-y", type=float, help="vertical crop position 0 (top) .. 1 (bottom); "
                    "default centre")
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--gop", type=int, default=8)
    ap.add_argument("--all-intra", action="store_true", help="every frame a keyframe (-g 1)")
    ap.add_argument("--crf", type=int, default=22)
    ap.add_argument("--duration", type=float, help="exact output seconds (tpad clone + trim)")
    ap.add_argument("--max-mb", type=float, default=6.0, help="per-file budget, decimal MB")
    ap.add_argument("--webm", action="store_true", help="also write a VP9 twin OUT.webm")
    ap.add_argument("--av1", action="store_true", help="also write an AV1 twin OUT.av1.mp4")
    ap.add_argument("--preset", default="slow", help="libx264 preset (default slow)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not a.out:
        ap.print_usage(sys.stderr); return 2
    if a.crop_y is not None and not 0.0 <= a.crop_y <= 1.0:
        raise V.ToolError("--crop-y must be within 0..1")
    ok, res = normalize(a.clip, a.out, a.trim, a.width, a.height, a.aspect, a.short_side,
                        a.crop_y, a.fps, a.gop, a.all_intra, a.crf, a.duration, a.max_mb,
                        a.webm, a.av1, a.preset)
    for r in res:
        print(f"{r['path']}  bytes={r['bytes']}  frames={r['frames']}  "
              f"duration={r['duration']}  {r['width']}x{r['height']}"
              f"{'  OVER_BUDGET' if r['over_budget'] else ''}")
    return 0 if ok else 1


if __name__ == "__main__":
    V.main_guard(main)
