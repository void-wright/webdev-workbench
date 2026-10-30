#!/usr/bin/env python3
"""
BLEND DETECTOR: finds soft dissolves (crossfades) hidden inside a generated take, plus the
biggest single-frame jumps (hard cuts).

Signature of a dissolve: a crossfade blends two sharp images, which LOWERS edge sharpness
(mean |horizontal gradient|) while inter-frame change stays ELEVATED. A sustained run (>= 4
frames) of motion > 1.6x the clip median AND sharpness < 0.93x the clip median is flagged.

Pure CPU (nothing here touches a card); frame rate probed instead of assumed; numpy maths;
argparse + a selftest with a positive control.

usage: python3 -B blend_detect.py CLIP [CLIP ...] [--motion-x 1.6] [--sharp-x 0.93]
       python3 -B blend_detect.py --selftest
Exit 0 no soft blend found / 1 a soft blend found / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

W, H = 160, 90


def analyse(path, motion_x=1.6, sharp_x=0.93, min_run=4):
    import numpy as np
    fps = V.probe(path)["fps"] or 24.0
    f = V.rgb_array(path, w=W, h=H).astype(np.float32).mean(axis=3)
    f = np.floor(f)                                  # grey bytes, as the original measured
    E = np.abs(np.diff(f, axis=2)).mean(axis=(1, 2))
    D = np.concatenate([[0.0], np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))])
    me, md = float(np.median(E)), float(np.median(D))
    flag = [(i / fps, D[i], E[i]) for i in range(len(f)) if D[i] > md * motion_x and E[i] < me * sharp_x]
    runs, cur = [], []
    for t, dd, ee in flag:
        if cur and t - cur[-1][0] <= 3.5 / fps:
            cur.append((t, dd, ee))
        else:
            if len(cur) >= min_run:
                runs.append(cur)
            cur = [(t, dd, ee)]
    if len(cur) >= min_run:
        runs.append(cur)
    blends = [{"start": round(r[0][0], 3), "end": round(r[-1][0], 3),
               "motion_x": round(float(np.mean([x[1] for x in r])) / md, 2) if md else None,
               "sharp_pct": round(100 * float(np.mean([x[2] for x in r])) / me, 1)} for r in runs]
    top = sorted(range(1, len(f)), key=lambda i: -D[i])[:5]
    jumps = [(round(i / fps, 3), round(float(D[i]) / md, 1) if md else None) for i in sorted(top)]
    return {"path": path, "frames": len(f), "median_edge": round(me, 2),
            "median_motion": round(md, 2), "blends": blends, "jumps": jumps}


def selftest():
    d = V.selftest_dir("blend_detect")
    try:
        # Texture, not test bars: a dissolve only lowers mean gradient where the two images'
        # edges do not line up, which is true of real footage (dense texture) but NOT of two
        # bar charts with aligned edges. So both shots are locked-off noise textures (an
        # integer-stepped pan was tried first and its jitter swamped the motion signal).
        def shot(name, seed):
            png = os.path.join(d, f"{name}.png")
            V.ff(["-f", "lavfi", "-i", "color=c=gray:size=1000x400", "-vf",
                  f"noise=alls=90:all_seed={seed},gblur=sigma=0.8", "-frames:v", "1", png])
            out = os.path.join(d, f"{name}.mp4")
            V.ff(["-loop", "1", "-framerate", "24", "-t", "2", "-i", png, "-vf",
                  "crop=640:360:x=40:y=20,format=yuv420p", "-c:v", "libx264",
                  "-preset", "veryfast", "-crf", "14", out])
            return out
        a, b = shot("a", 11), shot("b", 29)
        # positive control: a 1 s dissolve between two sharp textured shots -> must FAIL
        dis = os.path.join(d, "dissolve.mp4")
        V.ff(["-i", a, "-i", b, "-filter_complex",
              "[0:v][1:v]xfade=transition=fade:duration=1:offset=1,format=yuv420p[v]",
              "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", dis])
        rc, rd = analyse(a), analyse(dis)
        hit = rd["blends"] and rd["blends"][0]["start"] >= 0.9 and rd["blends"][0]["end"] <= 2.1
        ok = not rc["blends"] and bool(hit)
        span = f"{rd['blends'][0]['start']}-{rd['blends'][0]['end']}s" if rd["blends"] else "none"
        print(f"selftest blend_detect: clean blends={len(rc['blends'])} | control_dissolve="
              f"{'FAIL' if rd['blends'] else 'PASS'} blends={len(rd['blends'])} span={span} "
              f"-> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clips", nargs="*")
    ap.add_argument("--motion-x", type=float, default=1.6)
    ap.add_argument("--sharp-x", type=float, default=0.93)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clips:
        ap.print_usage(sys.stderr); return 2
    found = False
    for c in a.clips:
        r = analyse(V.need(c), a.motion_x, a.sharp_x)
        found = found or bool(r["blends"])
        print(f"{r['path']}  frames={r['frames']} median_edge={r['median_edge']} "
              f"median_motion={r['median_motion']} soft_blends={len(r['blends'])}")
        for bl in r["blends"]:
            print(f"  SOFT BLEND {bl['start']}-{bl['end']}s motion_x={bl['motion_x']} "
                  f"sharpness_pct={bl['sharp_pct']}")
        print("  biggest jumps: " + ", ".join(f"{t}s(x{x})" for t, x in r["jumps"]))
    return 1 if found else 0


if __name__ == "__main__":
    V.main_guard(main)
