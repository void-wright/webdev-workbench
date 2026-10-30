#!/usr/bin/env python3
"""
COLOR MATCH a passage clip toward a reference still (usually the stop it must land on), so
the scroll crossfade between poster and video does not pop.

Method: per-channel statistics transfer. The clip's R, G, B mean and standard deviation
(sampled across the whole clip, downscaled) are moved toward the still's:
    out_c = (in_c - mean_clip_c) * k_c + target_mean_c,   k_c = target_std_c / std_clip_c
with k clamped to [0.5, 2.0] and --strength 0..1 blending how far toward the still to go.
Applied as one exact per-channel affine LUT (ffmpeg lutrgb), one pass, no numpy LUT file.
The whole clip gets ONE correction, so the grade cannot flicker frame to frame.

PAPER LIFT (--paper-lift, white-ground journeys): after the match (or alone, without --ref), a
per-channel knee curve maps the clip's measured paper white (_vidlib.paper_stats white_rgb) to 255
and leaves everything below --knee (default 236) untouched, so a slightly grey or tinted paper
becomes the page's #FFF while the violets keep their values.

usage: python3 -B color_match.py CLIP --ref STILL OUT.mp4 [--strength 1.0] [--crf 16]
       python3 -B color_match.py CLIP OUT.mp4 --paper-lift [--knee 236]
       python3 -B color_match.py --selftest
Prints before/after per-channel mean deltas (clip - still, 0-255) and the gains. The output is
an intermediate (libx264 yuv420p, CRF 16, silent): run web_normalize after it.
Exit 0 / 1 (after delta exceeds --tolerance) / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def stats_clip(path):
    return V.channel_stats(path, w=160, fps_sample=4)


def stats_still(still, w, h):
    import tempfile
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        sc = os.path.join(td, "ref.png")
        V.ff(["-i", still, "-vf", V.cover_filter(w, h), "-frames:v", "1", sc])
        return V.channel_stats(sc, w=160)


def lift_exprs(white, knee=236.0):
    """Per channel: below the knee unchanged; from the knee to the measured white, stretched to 255."""
    out = []
    for ch, w in zip("rgb", white):
        if w <= knee + 2 or w >= 254.5:
            out.append(f"{ch}=val")
            continue
        s = (255.0 - knee) / (w - knee)
        out.append(f"{ch}='if(lt(val,{knee:.2f}),val,clip({knee:.2f}+(val-{knee:.2f})*{s:.5f},0,255))'")
    return out


def match(clip, ref, out, strength=1.0, crf=16, tolerance=4.0, paper_lift=False, knee=236.0):
    info = V.probe(clip)
    filters, gains, rep = [], [], {}
    affine = None
    if ref:
        V.need(ref)
        mc, sc = stats_clip(clip)
        mr, sr = stats_still(ref, info["width"], info["height"])
        exprs, affine = [], []
        for ch, a, sa, b, sb in zip("rgb", mc, sc, mr, sr):
            k_full = (sb / sa) if sa > 1e-6 else 1.0
            k = 1.0 + strength * (min(2.0, max(0.5, k_full)) - 1.0)
            tgt = a + strength * (b - a)
            gains.append(round(k, 4))
            affine.append((a, k, tgt))
            exprs.append(f"{ch}='clip((val-{a:.4f})*{k:.5f}+{tgt:.4f},0,255)'")
        filters.append("lutrgb=" + ":".join(exprs))
    if paper_lift:
        white = V.paper_stats(clip)["white_rgb"]
        if affine:  # the paper's white as the match leaves it
            white = [min(255.0, max(0.0, (w - a) * k + t)) for w, (a, k, t) in zip(white, affine)]
        filters.append("lutrgb=" + ":".join(lift_exprs(white, knee)))
        rep["paper_white_in"] = [round(x, 2) for x in white]
    vf = "format=rgb24," + ",".join(filters) + ",format=yuv420p"
    V.ff(["-i", clip, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium",
          "-crf", str(crf), "-pix_fmt", "yuv420p", out])
    if paper_lift:
        rep["paper_after"] = V.paper_stats(out)
    if ref:
        ma, _ = stats_clip(out)
        before = [round(x - y, 2) for x, y in zip(mc, mr)]
        after = [round(x - y, 2) for x, y in zip(ma, mr)]
        rep.update({"before_delta_rgb": before, "after_delta_rgb": after, "gain_rgb": gains,
                    "before_max": round(max(map(abs, before)), 2),
                    "after_max": round(max(map(abs, after)), 2)})
        # a paper lift moves the bright end away from an unlifted still on purpose: judge the match
        # on the still's own terms only without it
        rep["ok"] = paper_lift or max(map(abs, after)) <= tolerance
    else:
        rep["ok"] = True
    return rep


def selftest():
    d = V.selftest_dir("color_match")
    try:
        # the clip carries a warm cast the reference does not have
        cast = "colorchannelmixer=rr=1.15:bb=0.80"
        clip = V.lavfi_clip(os.path.join(d, "warm.mp4"), duration=2.0, extra_vf=cast)
        ref = V.lavfi_still(os.path.join(d, "ref.png"), t=1.0)
        r = match(clip, ref, os.path.join(d, "matched.mp4"))
        # positive control: the un-matched clip must FAIL the same tolerance
        control_fails = r["before_max"] > 4.0
        ok = r["ok"] and control_fails and r["after_max"] < r["before_max"] / 3
        print(f"selftest color_match: before_max={r['before_max']} after_max={r['after_max']} "
              f"before={r['before_delta_rgb']} after={r['after_delta_rgb']} "
              f"gains={r['gain_rgb']} | control_unmatched_exceeds_4="
              f"{'FAIL' if control_fails else 'PASS'} -> {'PASS' if ok else 'FAIL'}")
        if not ok:
            return 1
        # PAPER LIFT: a slightly grey, faintly cool paper with a violet wash -> paper 255, violet kept
        grey = V.lavfi_clip(os.path.join(d, "grey.mp4"), src="color=c=0xF1F0F5", duration=2.0,
                            extra_vf="drawbox=x=200:y=100:w=200:h=150:color=0x7B61C9:t=fill")
        before = V.paper_stats(grey)
        lifted = os.path.join(d, "lifted.mp4")
        r2 = match(grey, None, lifted, paper_lift=True)
        after = r2["paper_after"]
        # inside the violet box (x 50-100, y 25-62 at w=160)
        box = lambda p: V.rgb_array(p, w=160)[:, 32:56, 56:94].reshape(-1, 3).astype('float64').mean(axis=0)
        drift = float(abs(box(lifted) - box(grey)).max())
        # the re-encode alone moves the violet by about 1-2 (measured 2.00); a lift that touched it would move it far more
        ok2 = before["paper_p95_min"] < 248 and after["paper_p95_min"] >= 252 and drift <= 3.0
        print(f"selftest color_match --paper-lift: paper p95 {before['paper_p95_min']} -> "
              f"{after['paper_p95_min']} | violet drift {drift:.2f} (<=3) -> {'PASS' if ok2 else 'FAIL'}")
        return 0 if ok2 else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?"); ap.add_argument("out", nargs="?")
    ap.add_argument("--ref", help="reference still")
    ap.add_argument("--strength", type=float, default=1.0, help="0 = no change, 1 = full match")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--tolerance", type=float, default=4.0,
                    help="max |after| per-channel mean delta for exit 0 (default 4)")
    ap.add_argument("--paper-lift", action="store_true", help="white-ground: lift the paper to #FFF")
    ap.add_argument("--knee", type=float, default=236.0, help="values below this are untouched (default 236)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not a.out or not (a.ref or a.paper_lift):
        ap.print_usage(sys.stderr); return 2
    if not 0.0 <= a.strength <= 1.0:
        raise V.ToolError("--strength must be within 0..1")
    r = match(a.clip, a.ref, a.out, a.strength, a.crf, a.tolerance, a.paper_lift, a.knee)
    print(a.out)
    if a.ref:
        print(f"before_delta_rgb={r['before_delta_rgb']} max={r['before_max']}")
        print(f"after_delta_rgb={r['after_delta_rgb']} max={r['after_max']}")
        print(f"gain_rgb={r['gain_rgb']}")
    if a.paper_lift:
        print(f"paper_white_in={r['paper_white_in']} paper_after={r['paper_after']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    V.main_guard(main)
