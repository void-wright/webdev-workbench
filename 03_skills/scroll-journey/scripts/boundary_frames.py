#!/usr/bin/env python3
"""
Extract the FIRST and LAST frame of a clip as PNG: the seam endpoints of a web passage.

First frame: select=eq(n\\,0). Last frame: an -sseof seek (at most 1 s back) decoded with
-update 1, so the surviving PNG is the true final frame even when the demuxer seek snaps
early, and even on clips shorter than the seek window (the upstream method, hardened).
Extract boundaries from the NORMALISED clip, not from the source stills.

usage: python3 -B boundary_frames.py CLIP OUTDIR [--stem NAME]
       python3 -B boundary_frames.py --selftest
Writes OUTDIR/<stem>-first.png and OUTDIR/<stem>-last.png. Exit 0 ok / 1 fail / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402

HUE = "hue=H=n*0.7"   # every frame a different hue: adjacent frames are distinguishable


def extract(clip, outdir, stem=None):
    V.need(clip)
    os.makedirs(outdir, exist_ok=True)
    stem = stem or os.path.splitext(os.path.basename(clip))[0]
    f = V.first_frame(clip, os.path.join(outdir, f"{stem}-first.png"))
    l = V.last_frame(clip, os.path.join(outdir, f"{stem}-last.png"))
    return f, l


def selftest():
    d = V.selftest_dir("boundary_frames")
    try:
        ok = True
        # a clip that is red for 1 s then blue for 1 s: first must be red, last must be blue
        red = os.path.join(d, "red.mp4"); blue = os.path.join(d, "blue.mp4")
        V.lavfi_clip(red, src="color=c=red", duration=1.0)
        V.lavfi_clip(blue, src="color=c=blue", duration=1.0)
        rb = os.path.join(d, "rb.mp4")
        V.ff(["-i", red, "-i", blue, "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]",
              "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", rb])
        f, l = extract(rb, d)
        mf, _ = V.channel_stats(f); ml, _ = V.channel_stats(l)
        t1 = mf[0] > 200 and mf[2] < 60
        t2 = ml[2] > 200 and ml[0] < 60
        # positive control: claiming the last frame is red must FAIL
        control_fails = not (ml[0] > 200 and ml[2] < 60)
        # a 3-frame clip: robustness of the -sseof path on a clip shorter than the seek window
        short = os.path.join(d, "short.mp4")
        V.lavfi_clip(short, src="testsrc2", duration=3 / 24)
        fs, ls = extract(short, d)
        t3 = os.path.isfile(fs) and os.path.isfile(ls) and V.probe(short)["frames"] == 3
        # last frame of a 72-frame clip equals frame 71 of the source, not frame 70
        c = os.path.join(d, "c.mp4"); V.lavfi_clip(c, crf=10, extra_vf=HUE)
        _, lc = extract(c, d)
        ref71 = V.lavfi_still(os.path.join(d, "ref71.png"), t=71 / 24, extra_vf=HUE)
        ref70 = V.lavfi_still(os.path.join(d, "ref70.png"), t=70 / 24, extra_vf=HUE)
        # RGB distance, not SSIM: SSIM 'All' is luma-weighted and a hue step barely moves luma
        import numpy as np
        A = V.rgb_array(lc).astype(float)
        s71 = float(np.abs(A - V.rgb_array(ref71)).mean())
        s70 = float(np.abs(A - V.rgb_array(ref70)).mean())
        t4 = s71 < s70
        ok = t1 and t2 and control_fails and t3 and t4
        print(f"selftest boundary_frames: first_red={int(t1)} last_blue={int(t2)} "
              f"control_last_is_red_fails={int(control_fails)} short3={int(t3)} "
              f"last_rgbdist_f71={s71:.2f} f70={s70:.2f} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?"); ap.add_argument("outdir", nargs="?")
    ap.add_argument("--stem", help="output name stem (default: clip basename)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not a.outdir:
        ap.print_usage(sys.stderr); return 2
    f, l = extract(a.clip, a.outdir, a.stem)
    print(f); print(l)
    return 0


if __name__ == "__main__":
    V.main_guard(main)
