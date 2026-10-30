#!/usr/bin/env python3
"""
CONTINUITY AUDIT for a generated take: two independent hidden-cut detectors, a freeze count,
a motion profile, and an optional warm-ceiling meter.

Why two detectors: agreement between two independent methods is the evidence; either alone
is a claim.
  A) ffmpeg select='gt(scene,T)'  -> ffmpeg's own absolute scene score per flagged frame
  B) per-frame luma difference    -> frames above RATIO x the clip mean (cuts) and below 2%
                                     of the mean (frozen frames)
  C) warm-ceiling meter (--warm-times) -> mean(R)-mean(B) over the top third at named times;
     positive = warm light has reached the ceiling region

Scratch goes under the toolkit's scratch root; argparse + a selftest with a positive control.

usage: python3 -B continuity_audit.py CLIP [--threshold 0.05] [--ratio 4.0]
                                       [--warm-times 1.0 2.5 ...]
       python3 -B continuity_audit.py --selftest
Exit 0 no cut flagged by either detector / 1 a cut flagged / 2 usage.
"""
import os
import re
import statistics
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def scene_score(clip, thresh):
    p = V.ff(["-i", clip, "-filter_complex", f"select='gt(scene,{thresh})',metadata=print",
              "-an", "-f", "null", "-"], level="info")
    hits, t = [], None
    for line in p.stderr.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
        m = re.search(r"scene_score=([0-9.]+)", line)
        if m and t is not None:
            hits.append((t, float(m.group(1))))
    return hits


def luma_diff(clip, ratio):
    p = V.ff(["-i", clip, "-vf", "scale=320:-2,format=gray,tblend=all_mode=difference,"
              "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"],
             level="info")
    vals, t = [], None
    for line in p.stderr.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
        m = re.search(r"YAVG=([0-9.]+)", line)
        if m and t is not None:
            vals.append((t, float(m.group(1))))
    body = [v for _, v in vals][1:]          # frame 0 diff is meaningless
    mean = statistics.mean(body) if body else 0.0
    cuts = [(t, v, v / mean) for t, v in vals[1:] if mean and v > ratio * mean]
    freeze = [(t, v, v / mean) for t, v in vals[1:] if mean and v < 0.02 * mean]
    return mean, cuts, freeze, vals


def warm_ceiling(clip, times):
    import numpy as np
    from PIL import Image
    out = []
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as d:
        for t in times:
            f = os.path.join(d, "f.png")
            V.ff(["-ss", f"{t:.3f}", "-i", clip, "-frames:v", "1", f])
            a = np.asarray(Image.open(f).convert("RGB")).astype(float)
            top = a[: a.shape[0] // 3]
            out.append((t, float(top[:, :, 0].mean() - top[:, :, 2].mean())))
    return out


def audit(clip, thresh=0.05, ratio=4.0):
    hits = scene_score(V.need(clip), thresh)
    mean, cuts, freeze, vals = luma_diff(clip, ratio)
    return {"scene_hits": hits, "luma_mean": mean, "luma_cuts": cuts, "freeze": freeze,
            "vals": vals}


def report(clip, r, thresh, ratio, warm_times):
    i = V.probe(clip)
    print(f"{clip}  {i['vcodec']} {i['pix_fmt']} {i['width']}x{i['height']} fps={i['fps']:.3f} "
          f"frames={i['frames']} duration={i['duration']:.3f}")
    print(f"A scene_score>{thresh}: {len(r['scene_hits'])}")
    for t, s in r["scene_hits"]:
        print(f"  {t:7.3f}s  scene_score={s:.3f}")
    print(f"B luma_diff>{ratio}x mean ({r['luma_mean']:.3f}): {len(r['luma_cuts'])}")
    for t, v, x in r["luma_cuts"]:
        print(f"  {t:7.3f}s  diff={v:.2f}  {x:.2f}x")
    print(f"frozen_frames(<2% mean): {len(r['freeze'])}")
    q = [v for _, v in r["vals"][1:]]
    n = len(q) // 6
    if n:
        print("motion profile (6 windows, % of clip mean):")
        for k in range(6):
            w = q[k * n:(k + 1) * n]
            print(f"  window {k + 1}: {statistics.mean(w):6.2f}  "
                  f"{100 * statistics.mean(w) / r['luma_mean']:5.1f}%")
    if warm_times:
        for t, v in warm_ceiling(clip, warm_times):
            print(f"warm_ceiling {t:.3f}s R-B={v:+.2f}")
    a_t = {round(t, 2) for t, _ in r["scene_hits"]}
    b_t = {round(t, 2) for t, _, _ in r["luma_cuts"]}
    print(f"cuts A={len(a_t)} B={len(b_t)} agree={len(a_t & b_t)}")


def selftest():
    d = V.selftest_dir("continuity_audit")
    try:
        clean = V.lavfi_clip(os.path.join(d, "clean.mp4"), duration=3.0)
        a = V.lavfi_clip(os.path.join(d, "a.mp4"), duration=1.5)
        b = V.lavfi_clip(os.path.join(d, "b.mp4"), src="smptehdbars", duration=1.5)
        cut = os.path.join(d, "cut.mp4")
        V.ff(["-i", a, "-i", b, "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]",
              "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", cut])
        rc = audit(clean); rx = audit(cut)
        a_t = [round(t, 2) for t, _ in rx["scene_hits"]]
        b_t = [round(t, 2) for t, _, _ in rx["luma_cuts"]]
        agree = bool(set(a_t) & set(b_t)) and 1.5 in a_t
        clean_ok = not rc["scene_hits"] and not rc["luma_cuts"]
        ok = clean_ok and agree
        print(f"selftest continuity_audit: clean A={len(rc['scene_hits'])} "
              f"B={len(rc['luma_cuts'])} | control_hidden_cut="
              f"{'FAIL' if (a_t or b_t) else 'PASS'} A={a_t} B={b_t} agree={int(agree)} "
              f"-> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--threshold", type=float, default=0.05, help="ffmpeg scene threshold")
    ap.add_argument("--ratio", type=float, default=4.0, help="luma diff cut ratio x mean")
    ap.add_argument("--warm-times", type=float, nargs="*", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip:
        ap.print_usage(sys.stderr); return 2
    r = audit(a.clip, a.threshold, a.ratio)
    report(a.clip, r, a.threshold, a.ratio, a.warm_times)
    return 1 if (r["scene_hits"] or r["luma_cuts"]) else 0


if __name__ == "__main__":
    V.main_guard(main)
