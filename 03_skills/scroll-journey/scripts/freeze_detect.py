#!/usr/bin/env python3
"""
FREEZE DETECTOR: finds spans where the picture stops moving.

Median inter-frame motion cannot tell "the world is stable" from "the subject stopped". This
measures mean absolute inter-frame change (grey, downscaled) over the frame, optionally with a
box MASKED OUT (--mask) so a still frame with one animated region (a talking mouth, a
spinning logo) still reads as FROZEN, which is what it is.

Frame rate is probed (never assumed), the mask is optional, the maths is numpy-vectorised,
and a selftest with a positive control is built in.

usage: python3 -B freeze_detect.py CLIP [CLIP ...] [--threshold 1.0] [--min-span 0.5]
                                    [--mask X0,Y0,X1,Y1]
       python3 -B freeze_detect.py --selftest
--mask takes fractions of width/height, e.g. 0.30,0.15,0.70,0.95 (a centred speaker box).
Prints frozen seconds, span count and each span. Exit 0 no frozen span / 1 any / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

W, H = 160, 90


def motion(path, mask=None):
    import numpy as np
    a = V.rgb_array(path, w=W, h=H).astype(np.float32).mean(axis=3)   # grey
    m = np.ones((H, W), bool)
    if mask:
        x0, y0, x1, y1 = mask
        m[int(H * y0):int(H * y1), int(W * x0):int(W * x1)] = False
    d = np.abs(np.diff(a, axis=0))
    return (d * m).sum(axis=(1, 2)) / max(int(m.sum()), 1)


def spans_of(d, fps, thr=1.0, min_span=0.5):
    frozen = d < thr
    spans, i = [], 0
    while i < len(frozen):
        if frozen[i]:
            j = i
            while j < len(frozen) and frozen[j]:
                j += 1
            if (j - i) / fps >= min_span:
                spans.append((i / fps, (j - i) / fps))
            i = j
        else:
            i += 1
    return spans


def detect(path, thr=1.0, min_span=0.5, mask=None):
    fps = V.probe(path)["fps"] or 24.0
    d = motion(path, mask)
    sp = spans_of(d, fps, thr, min_span)
    return {"path": path, "seconds": round(len(d) / fps, 3), "frozen_seconds":
            round(sum(s for _, s in sp), 3), "spans": [(round(a, 3), round(b, 3)) for a, b in sp]}


def selftest():
    d = V.selftest_dir("freeze_detect")
    try:
        clean = V.lavfi_clip(os.path.join(d, "clean.mp4"), duration=3.0)
        # positive control: 1 s of motion, then the last frame held for 1.5 s -> must FAIL
        frozen = os.path.join(d, "frozen.mp4")
        V.ff(["-f", "lavfi", "-i", "testsrc2=size=640x360:rate=24:duration=1",
              "-vf", "tpad=stop_mode=clone:stop_duration=1.5,format=yuv420p",
              "-c:v", "libx264", "-preset", "veryfast", frozen])
        rc, rf = detect(clean), detect(frozen)
        ok = not rc["spans"] and len(rf["spans"]) == 1 and abs(rf["frozen_seconds"] - 1.5) < 0.1
        print(f"selftest freeze_detect: clean spans={len(rc['spans'])} | control_frozen="
              f"{'FAIL' if rf['spans'] else 'PASS'} spans={len(rf['spans'])} "
              f"frozen_s={rf['frozen_seconds']} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clips", nargs="*")
    ap.add_argument("--threshold", type=float, default=1.0,
                    help="mean |grey diff| below this = frozen (0-255 scale, default 1.0)")
    ap.add_argument("--min-span", type=float, default=0.5, help="seconds (default 0.5)")
    ap.add_argument("--mask", help="X0,Y0,X1,Y1 fractions to ignore (e.g. a speaker box)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clips:
        ap.print_usage(sys.stderr); return 2
    mask = None
    if a.mask:
        try:
            mask = [float(x) for x in a.mask.split(",")]
            assert len(mask) == 4
        except (ValueError, AssertionError):
            raise V.ToolError("--mask wants X0,Y0,X1,Y1")
    anyf = False
    for c in a.clips:
        r = detect(V.need(c), a.threshold, a.min_span, mask)
        anyf = anyf or bool(r["spans"])
        print(f"{r['path']}  frozen={r['frozen_seconds']}s of {r['seconds']}s  "
              f"spans={len(r['spans'])}")
        for st, ln in r["spans"]:
            print(f"  frozen {st:.3f}s for {ln:.3f}s")
    return 1 if anyf else 0


if __name__ == "__main__":
    V.main_guard(main)
