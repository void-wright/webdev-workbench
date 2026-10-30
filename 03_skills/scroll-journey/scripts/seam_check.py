#!/usr/bin/env python3
"""
SEAM CHECK for one web passage: does the clip start ON the start still and end ON the end
still, closely enough that a scroll crossfade over the boundary reads as one camera take?

Measures (stills are cover-scaled to the clip size; both sides converted to yuv420p):
  - SSIM  first frame vs --start still, last frame vs --end still      (ffmpeg ssim, 'All')
  - mean colour difference at both ends: per-channel |mean(frame) - mean(still)|, 0-255
  - inside the clip: freezedetect spans (informational) and scdet hidden-cut count
  - whether an audio stream is present (web passages ship silent)
  - with --paper (white-ground journeys): the paper's level and tint over the whole clip
    (_vidlib.paper_stats): the worst frame's p95 luminance must be >= --paper-min (default 248)
    and the brightest decile's tint <= --paper-tint (default 4). A grey veil or a cast is
    REPAIRABLE by color_match --paper-lift; paper darker than --paper-floor (235) is FAIL.

Verdict:
  PASS        both SSIMs >= --min-ssim, colour deltas <= --max-color, no cuts, no audio
  REPAIRABLE  both SSIMs >= --repair-floor and no cuts, but something above is off
              (seam_repair.py fixes SSIM; color_match.py fixes colour; web_normalize -an fixes audio)
  FAIL        an end below --repair-floor (the clip lands somewhere else), or a hidden cut

usage: python3 -B seam_check.py CLIP --start STILL --end STILL [--min-ssim 0.90] [--paper]
       python3 -B seam_check.py --selftest
Either --start or --end may be omitted (that end is not judged). JSON report on stdout
(and --json-out FILE). Exit 0 PASS / 1 REPAIRABLE or FAIL / 2 usage.
"""
import os
import re
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def cut_and_freeze(clip, scd_threshold=10.0, freeze_noise=0.001, freeze_min=0.5):
    p = V.ff(["-i", clip, "-an", "-vf",
              f"freezedetect=n={freeze_noise}:d={freeze_min},scdet=threshold={scd_threshold}",
              "-f", "null", "-"], level="info")
    cuts = [float(t) for t in re.findall(r"lavfi\.scd\.time:\s*([0-9.]+)", p.stderr)]
    freezes = len(re.findall(r"freeze_start", p.stderr))
    fdur = sum(float(x) for x in re.findall(r"freeze_duration:\s*([0-9.]+)", p.stderr))
    return cuts, freezes, fdur


def check(clip, start=None, end=None, min_ssim=0.90, repair_floor=0.75, max_color=8.0,
          scd_threshold=10.0, paper=False, paper_min=248.0, paper_tint=4.0, paper_floor=235.0):
    info = V.probe(clip)
    w, h = info["width"], info["height"]
    rep = {"clip": clip, "width": w, "height": h, "fps": round(info["fps"], 3),
           "frames": info["frames"], "duration": round(info["duration"], 3),
           "has_audio": info["has_audio"]}
    with tempfile.TemporaryDirectory(dir=V.scratch_root()) as td:
        ends = {}
        if start:
            ends["start"] = (V.first_frame(clip, os.path.join(td, "first.png")), V.need(start))
        if end:
            ends["end"] = (V.last_frame(clip, os.path.join(td, "last.png")), V.need(end))
        for k, (frame, still) in ends.items():
            ssim = V.ssim_images(frame, still, w, h)
            # colour: the still cover-scaled to clip size, then channel means compared
            sc = os.path.join(td, f"still_{k}.png")
            V.ff(["-i", still, "-vf", V.cover_filter(w, h), "-frames:v", "1", sc])
            mf, _ = V.channel_stats(frame); ms, _ = V.channel_stats(sc)
            delta = [round(a - b, 2) for a, b in zip(mf, ms)]
            rep[k] = {"still": still, "ssim": round(ssim, 4), "color_delta_rgb": delta,
                      "color_delta_max": round(max(abs(x) for x in delta), 2)}
    cuts, freezes, fdur = cut_and_freeze(clip, scd_threshold)
    rep["scene_cuts"] = len(cuts)
    rep["scene_cut_times"] = [round(t, 3) for t in cuts]
    rep["freeze_spans"] = freezes
    rep["freeze_seconds"] = round(fdur, 3)

    reasons = []
    hard = False
    for k in ("start", "end"):
        if k in rep:
            s = rep[k]["ssim"]
            if s < repair_floor:
                hard = True; reasons.append(f"{k}_ssim<{repair_floor}")
            elif s < min_ssim:
                reasons.append(f"{k}_ssim<{min_ssim}")
            if rep[k]["color_delta_max"] > max_color:
                reasons.append(f"{k}_color>{max_color}")
    if cuts:
        hard = True; reasons.append("scene_cut")
    if info["has_audio"]:
        reasons.append("audio_stream")
    if paper:
        ps = V.paper_stats(clip)
        rep["paper"] = ps
        if ps["paper_p95_min"] < paper_floor:
            hard = True; reasons.append(f"paper_dark<{paper_floor}")
        elif ps["paper_p95_min"] < paper_min:
            reasons.append(f"paper_grey<{paper_min}")
        if ps["paper_tint_max"] > paper_tint:
            reasons.append(f"paper_tint>{paper_tint}")
    rep["verdict"] = "FAIL" if hard else ("REPAIRABLE" if reasons else "PASS")
    rep["reasons"] = reasons
    return rep


def selftest():
    d = V.selftest_dir("seam_check")
    try:
        HUE = "hue=H=n*0.05"
        clip = V.lavfi_clip(os.path.join(d, "clip.mp4"), duration=3.0, crf=20, extra_vf=HUE)
        s0 = V.lavfi_still(os.path.join(d, "s0.png"), t=0, extra_vf=HUE)
        s1 = V.lavfi_still(os.path.join(d, "s1.png"), t=71 / 24, extra_vf=HUE)
        good = check(clip, s0, s1)
        # positive control 1: the end still is a DIFFERENT image -> must FAIL
        wrong = V.lavfi_still(os.path.join(d, "wrong.png"), src="smptehdbars")
        bad = check(clip, s0, wrong)
        # positive control 2: a hidden hard cut inside the clip -> must FAIL
        a = V.lavfi_clip(os.path.join(d, "a.mp4"), duration=1.5)
        b = V.lavfi_clip(os.path.join(d, "b.mp4"), src="smptehdbars", duration=1.5)
        cut = os.path.join(d, "cut.mp4")
        V.ff(["-i", a, "-i", b, "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]",
              "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", cut])
        cutrep = check(cut, None, None)
        # positive control 3 (--paper): white paper with a violet wash passes; the same, greyed, does not
        paper = V.lavfi_clip(os.path.join(d, "paper.mp4"), src="color=c=white", duration=2.0,
                             extra_vf="drawbox=x=200:y=100:w=200:h=150:color=0x7B61C9:t=fill")
        grey = V.lavfi_clip(os.path.join(d, "grey.mp4"), src="color=c=0xEEEDF1", duration=2.0,
                            extra_vf="drawbox=x=200:y=100:w=200:h=150:color=0x7B61C9:t=fill")
        pw = check(paper, None, None, paper=True)
        pg = check(grey, None, None, paper=True)
        ok = (good["verdict"] == "PASS" and bad["verdict"] == "FAIL" and cutrep["verdict"] == "FAIL"
              and pw["verdict"] == "PASS" and pg["verdict"] != "PASS")
        print(f"selftest seam_check: matched={good['verdict']} start_ssim={good['start']['ssim']} "
              f"end_ssim={good['end']['ssim']} cuts={good['scene_cuts']} | "
              f"control_wrong_end={bad['verdict']} end_ssim={bad['end']['ssim']} | "
              f"control_hidden_cut={cutrep['verdict']} cuts={cutrep['scene_cuts']} | "
              f"paper_white={pw['verdict']} p95={pw['paper']['paper_p95_min']} | "
              f"control_paper_grey={pg['verdict']} p95={pg['paper']['paper_p95_min']} "
              f"-> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--start", help="still the clip must START on")
    ap.add_argument("--end", help="still the clip must END on")
    ap.add_argument("--min-ssim", type=float, default=0.90)
    ap.add_argument("--repair-floor", type=float, default=0.75,
                    help="below this an end is not repairable by a micro-crossfade (default 0.75; unrelated images measured 0.62)")
    ap.add_argument("--max-color", type=float, default=8.0,
                    help="max per-channel mean colour delta, 0-255 (default 8)")
    ap.add_argument("--scd-threshold", type=float, default=10.0, help="scdet threshold 0-100")
    ap.add_argument("--paper", action="store_true", help="white-ground: judge the paper's level and tint")
    ap.add_argument("--paper-min", type=float, default=248.0)
    ap.add_argument("--paper-tint", type=float, default=4.0)
    ap.add_argument("--paper-floor", type=float, default=235.0)
    ap.add_argument("--json-out", help="also write the report here")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.clip or not (a.start or a.end or a.paper):
        ap.print_usage(sys.stderr); return 2
    rep = check(a.clip, a.start, a.end, a.min_ssim, a.repair_floor, a.max_color, a.scd_threshold,
                a.paper, a.paper_min, a.paper_tint, a.paper_floor)
    V.emit(rep)
    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(rep, fh, indent=1)
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    V.main_guard(main)
