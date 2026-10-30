#!/usr/bin/env python3
"""
SEAM REPAIR: make a passage clip end EXACTLY on its end still (and/or start exactly on its
start still), so the scroll handoff between poster and video is a non-event.

Tail (--end STILL):
  1. per-frame SSIM of the clip vs the still (ffmpeg ssim stats) over the last --search frames;
  2. trim the clip at the best-matching frame (drops any overshoot past the landing);
  3. bake a micro-crossfade (xfade fade, --fade-frames long) from the clip onto the still, held
     one extra frame, so the FINAL frame is the still itself.
Head (--start STILL): the mirror image. Search the first --search frames, start the clip at
the best match, and open on the still for one frame, crossfading into the clip.

usage: python3 -B seam_repair.py CLIP OUT.mp4 [--end STILL] [--start STILL]
                                  [--fade-frames 8] [--search 24] [--crf 16]
       python3 -B seam_repair.py --selftest
Prints the chosen frame indices + SSIMs, frame counts, and the post-repair seam SSIMs.
The output is an intermediate (libx264 yuv420p, CRF 16, silent). Exit 0 / 1 / 2.
"""
import os
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def best_index(series, lo, hi):
    lo, hi = max(0, lo), min(len(series) - 1, hi)
    if hi < lo:
        raise RuntimeError("search window empty")
    i = max(range(lo, hi + 1), key=lambda k: series[k])
    return i, series[i]


def repair(clip, out, end=None, start=None, fade_frames=8, search=24, crf=16):
    if not (end or start):
        raise V.ToolError("need --end and/or --start")
    info = V.probe(clip)
    n, fps, w, h = info["frames"], info["fps"], info["width"], info["height"]
    F = int(fade_frames)
    if F < 1:
        raise V.ToolError("--fade-frames must be >= 1")
    rep = {"clip": clip, "frames_in": n, "fps": round(fps, 3)}
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        b0, b1 = 0, n - 1
        if start:
            s = V.ssim_series(clip, V.need(start), td)
            b0, v = best_index(s, 0, search - 1)
            rep["start_best_frame"] = b0; rep["start_best_ssim"] = round(v, 4)
            rep["start_frame0_ssim"] = round(s[0], 4)
        if end:
            s = V.ssim_series(clip, V.need(end), td)
            b1, v = best_index(s, n - search, n - 1)
            rep["end_best_frame"] = b1; rep["end_best_ssim"] = round(v, 4)
            rep["end_lastframe_ssim"] = round(s[-1], 4)
        if b1 - b0 + 1 < 2 * F + 2:
            raise RuntimeError("clip too short between the chosen frames for the fade")
        lenA = b1 - b0 + 1
        args = ["-i", clip]
        g = [f"[0:v]trim=start_frame={b0}:end_frame={b1 + 1},setpts=N/({fps}*TB),"
             f"format=yuv420p,settb=AVTB[a]"]
        cur, cur_len, k = "a", lenA, 1
        still_chain = (lambda idx, lbl: f"[{idx}:v]{V.cover_filter(w, h)},format=yuv420p,"
                       f"trim=end_frame={F + 1},setpts=N/({fps}*TB),settb=AVTB[{lbl}]")
        D = F / fps
        if start:
            args += ["-loop", "1", "-framerate", str(fps), "-i", start]
            g.append(still_chain(k, "s"))
            # still frame 0 pure, then F blended frames into the clip. Offsets are placed half
            # a frame early so float rounding cannot shift the transition by a frame.
            g.append(f"[s][{cur}]xfade=transition=fade:duration={D:.6f}:"
                     f"offset={(0.5) / fps:.6f}[h]")
            cur, cur_len, k = "h", 1 + cur_len, k + 1
        if end:
            args += ["-loop", "1", "-framerate", str(fps), "-i", end]
            g.append(still_chain(k, "e"))
            g.append(f"[{cur}][e]xfade=transition=fade:duration={D:.6f}:"
                     f"offset={(cur_len - F - 0.5) / fps:.6f}[t]")
            cur, cur_len = "t", cur_len + 1
        g.append(f"[{cur}]setpts=N/({fps}*TB)[o]")
        V.ff(args + ["-filter_complex", ";".join(g), "-map", "[o]", "-an", "-r", str(fps),
                     "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
                     "-pix_fmt", "yuv420p", out])
        o = V.probe(out)
        rep["frames_out"] = o["frames"]; rep["frames_expected"] = cur_len
        rep["out"] = out
        if end:
            rep["out_end_ssim"] = round(V.ssim_images(
                V.last_frame(out, os.path.join(td, "ol.png")), end, w, h), 4)
        if start:
            rep["out_start_ssim"] = round(V.ssim_images(
                V.first_frame(out, os.path.join(td, "of.png")), start, w, h), 4)
    return rep


def selftest():
    d = V.selftest_dir("seam_repair")
    try:
        import seam_check as SC
        HUE = "hue=H=n*0.05"
        clip = V.lavfi_clip(os.path.join(d, "clip.mp4"), duration=3.0, crf=18, extra_vf=HUE)
        # the take overshoots its landing by 9 frames and starts 3 frames early
        end = V.lavfi_still(os.path.join(d, "end.png"), t=62 / 24, extra_vf=HUE)
        start = V.lavfi_still(os.path.join(d, "start.png"), t=3 / 24, extra_vf=HUE)
        before = SC.check(clip, start, end, min_ssim=0.99)
        out = os.path.join(d, "repaired.mp4")
        r = repair(clip, out, end=end, start=start, fade_frames=8, search=24)
        after = SC.check(out, start, end, min_ssim=0.99)
        # positive control: the unrepaired clip must FAIL the 0.99 bar at the end
        control_fails = before["end"]["ssim"] < 0.99
        ok = (after["end"]["ssim"] >= 0.99 and after["start"]["ssim"] >= 0.99 and control_fails
              and abs(r["end_best_frame"] - 62) <= 1 and abs(r["start_best_frame"] - 3) <= 1
              and r["frames_out"] == r["frames_expected"] and after["scene_cuts"] == 0)
        print(f"selftest seam_repair: best_end={r['end_best_frame']} best_start="
              f"{r['start_best_frame']} frames {r['frames_in']}->{r['frames_out']} "
              f"(expected {r['frames_expected']}) | after end_ssim={after['end']['ssim']} "
              f"start_ssim={after['start']['ssim']} cuts={after['scene_cuts']} | "
              f"control_unrepaired_end_ssim={before['end']['ssim']} "
              f"{'FAIL' if control_fails else 'PASS'}@0.99 -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?"); ap.add_argument("out", nargs="?")
    ap.add_argument("--end", help="still the clip must end exactly on")
    ap.add_argument("--start", help="still the clip must start exactly on")
    ap.add_argument("--fade-frames", type=int, default=8)
    ap.add_argument("--search", type=int, default=24,
                    help="frames searched at each end for the best match (default 24)")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--min-ssim", type=float, default=0.99,
                    help="post-repair seam SSIM required for exit 0 (default 0.99)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not a.out or not (a.end or a.start):
        ap.print_usage(sys.stderr); return 2
    r = repair(a.clip, a.out, a.end, a.start, a.fade_frames, a.search, a.crf)
    print(r["out"])
    for k in ("start_best_frame", "start_best_ssim", "start_frame0_ssim", "end_best_frame",
              "end_best_ssim", "end_lastframe_ssim", "frames_in", "frames_out",
              "out_start_ssim", "out_end_ssim"):
        if k in r:
            print(f"{k}={r[k]}")
    ok = all(r.get(k, 1.0) >= a.min_ssim for k in ("out_start_ssim", "out_end_ssim"))
    return 0 if ok else 1


if __name__ == "__main__":
    V.main_guard(main)
