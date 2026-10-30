#!/usr/bin/env python3
"""
LOOP SEAL a banner clip so it loops without a jump, then web-normalise it and make its poster.

The seal: with F = --fade seconds, the output is clip[F .. end] whose last F seconds crossfade
(xfade fade) into clip[0 .. F]. The output's final frame is therefore (almost) clip frame F-1,
and the loop restarts on clip frame F: adjacent frames, no seam. Length = original - F.
The sealed clip is then normalised exactly as web_normalize does (it calls it), and frame 0
is written as a WebP poster no larger than --poster-kb (default 300 KB).

usage: python3 -B loop_seal.py CLIP OUT.mp4 [--fade 1.0] [--width 1280 --height 720 |
                                --aspect 16:9] [--fps 24] [--gop 8 | --all-intra] [--crf 22]
                                [--max-mb 6] [--poster-kb 300]
       python3 -B loop_seal.py --selftest
Prints the loop SSIM (last frame vs first frame) before and after, bytes, and the poster path.
The seam passes when last-vs-first SSIM is no worse than the clip's own worst adjacent-frame
SSIM (minus 0.01): an invisible seam is one indistinguishable from an ordinary frame step.
Exit 0 / 1 (over budget, poster too big, or seam worse than a frame step) / 2 usage.
"""
import os
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402
import web_normalize as WN  # noqa: E402


def loop_ssim(clip, td, tag):
    f = V.first_frame(clip, os.path.join(td, f"{tag}_first.png"))
    l = V.last_frame(clip, os.path.join(td, f"{tag}_last.png"))
    return V.ssim_images(l, f)


def poster(clip, out_webp, max_kb=300):
    from PIL import Image
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        png = V.first_frame(clip, os.path.join(td, "p.png"))
        im = Image.open(png).convert("RGB")
        for q in (86, 80, 74, 68, 60, 50, 40, 30):
            im.save(out_webp, "WEBP", quality=q, method=6)
            if os.path.getsize(out_webp) <= max_kb * 1000:
                return out_webp, q, os.path.getsize(out_webp)
    return out_webp, q, os.path.getsize(out_webp)


def seal(clip, out, fade=1.0, poster_kb=300, **norm):
    info = V.probe(clip)
    n, fps = info["frames"], info["fps"]
    F = int(round(fade * fps))
    if F < 1 or n < 2 * F + 2:
        raise V.ToolError(f"--fade {fade}s needs a clip longer than {2 * fade:.2f}s")
    lenA = n - F
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        before = loop_ssim(clip, td, "in")
        sealed = os.path.join(td, "sealed.mp4")
        g = (f"[0:v]split[x][y];"
             f"[x]trim=start_frame={F},setpts=N/({fps}*TB),format=yuv420p,settb=AVTB[a];"
             f"[y]trim=end_frame={F},setpts=N/({fps}*TB),format=yuv420p,settb=AVTB[b];"
             f"[a][b]xfade=transition=fade:duration={F / fps:.6f}:"
             f"offset={(lenA - F - 0.5) / fps:.6f},setpts=N/({fps}*TB)[o]")
        V.ff(["-i", clip, "-filter_complex", g, "-map", "[o]", "-an", "-r", str(fps),
              "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
              sealed])
        sealed_frames = V.probe(sealed)["frames"]
        ok, res = WN.normalize(sealed, out, **norm)
        after = loop_ssim(out, td, "out")
        adj_med, adj_min = V.adjacent_ssim(out, td)
    pw, q, pb = poster(out, os.path.splitext(out)[0] + ".poster.webp", poster_kb)
    return {"out": out, "frames_in": n, "fade_frames": F, "frames_sealed": sealed_frames,
            "frames_expected": lenA, "loop_ssim_before": round(before, 4),
            "loop_ssim_after": round(after, 4), "adjacent_ssim_median": round(adj_med, 4),
            "adjacent_ssim_min": round(adj_min, 4),
            "seam_ok": after >= adj_min - 0.01, "bytes": res[0]["bytes"],
            "frames_out": res[0]["frames"], "budget_ok": ok, "poster": pw,
            "poster_bytes": pb, "poster_quality": q, "poster_ok": pb <= poster_kb * 1000}


def selftest():
    d = V.selftest_dir("loop_seal")
    try:
        import verify_web_media as VWM
        clip = V.lavfi_clip(os.path.join(d, "banner.mp4"), duration=4.0,
                            extra_vf="hue=H=n*0.03")
        out = os.path.join(d, "banner_loop.mp4")
        r = seal(clip, out, fade=1.0, fps=24, gop=8, preset="veryfast")
        v = VWM.verify(out, max_mb=6, expect_fps=24, expect_gop=8)
        # the bar is the clip's own worst ordinary frame step (minus 0.01), not a constant:
        # adjacent frames of this content measured ~0.94 median, so 0.95 would be miscalibrated.
        bar = r["adjacent_ssim_min"] - 0.01
        # positive control: the UNSEALED clip's loop point must FAIL the same bar
        control_fails = r["loop_ssim_before"] < bar
        ok = (r["seam_ok"] and control_fails and r["budget_ok"]
              and r["poster_ok"] and v["verdict"] == "PASS"
              and r["frames_sealed"] == r["frames_expected"] == r["frames_out"])
        print(f"selftest loop_seal: frames {r['frames_in']}->{r['frames_out']} "
              f"(expected {r['frames_expected']}) loop_ssim_after={r['loop_ssim_after']} "
              f"adjacent_min={r['adjacent_ssim_min']} median={r['adjacent_ssim_median']} "
              f"bytes={r['bytes']} verify={v['verdict']} poster_bytes={r['poster_bytes']} "
              f"q={r['poster_quality']} | control_unsealed_loop_ssim={r['loop_ssim_before']} "
              f"{'FAIL' if control_fails else 'PASS'}@{bar:.4f} -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?"); ap.add_argument("out", nargs="?")
    ap.add_argument("--fade", type=float, default=1.0, help="crossfade seconds (default 1.0)")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--aspect"); ap.add_argument("--short-side", type=int, default=720)
    ap.add_argument("--crop-y", type=float)
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--gop", type=int, default=8)
    ap.add_argument("--all-intra", action="store_true")
    ap.add_argument("--crf", type=int, default=22)
    ap.add_argument("--max-mb", type=float, default=6.0)
    ap.add_argument("--poster-kb", type=int, default=300)
    ap.add_argument("--min-ssim", type=float,
                    help="optional absolute floor for the sealed loop SSIM; by default the seam "
                    "must be no worse than the clip's own worst frame step (minus 0.01)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not a.out:
        ap.print_usage(sys.stderr); return 2
    r = seal(a.clip, a.out, a.fade, a.poster_kb, width=a.width, height=a.height,
             aspect=a.aspect, short_side=a.short_side, crop_y=a.crop_y, fps=a.fps, gop=a.gop,
             all_intra=a.all_intra, crf=a.crf, max_mb=a.max_mb)
    print(r["out"])
    print(f"bytes={r['bytes']} frames={r['frames_out']} fade_frames={r['fade_frames']}")
    print(f"loop_ssim_before={r['loop_ssim_before']} loop_ssim_after={r['loop_ssim_after']} "
          f"adjacent_ssim_min={r['adjacent_ssim_min']} median={r['adjacent_ssim_median']}")
    print(f"{r['poster']} bytes={r['poster_bytes']} quality={r['poster_quality']}")
    ok = r["budget_ok"] and r["poster_ok"] and r["seam_ok"] and \
        (a.min_ssim is None or r["loop_ssim_after"] >= a.min_ssim)
    return 0 if ok else 1


if __name__ == "__main__":
    V.main_guard(main)
