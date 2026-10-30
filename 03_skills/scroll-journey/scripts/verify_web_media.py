#!/usr/bin/env python3
"""
VERIFY WEB MEDIA: the last gate before passage clips ship. Every check is MEASURED from the
file, never read from a manifest:

  codec       h264 for *.mp4 (av1 for *.av1.mp4; vp9/av1 for *.webm)
  pix_fmt     yuv420p
  audio       NO audio stream (scrubbed passages are silent)
  faststart   top-level 'moov' atom before 'mdat' (mp4 only; read from the file's atom walk)
  GOP         keyframe interval measured from ffprobe packet flags; max interval <= --expect-gop
  fps         measured average frame rate == --expect-fps (when given)
  bytes       <= --max-mb (decimal MB)
  duration    reported

usage: python3 -B verify_web_media.py DIR_OR_FILES... [--max-mb 6] [--expect-fps 24]
                                       [--expect-gop 8]
       python3 -B verify_web_media.py --selftest
A directory is scanned (not recursively) for *.mp4 and *.webm. One line per file, then a FAIL
list. Exit 0 all PASS / 1 any FAIL / 2 usage.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _vidlib as V  # noqa: E402


def keyframe_intervals(path):
    p = V.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "packet=flags", "-of", "csv=p=0", path])
    flags = [ln.strip() for ln in p.stdout.splitlines() if ln.strip()]
    keys = [i for i, f in enumerate(flags) if "K" in f]
    if not keys:
        return [], len(flags)
    bounds = keys + [len(flags)]
    return [bounds[i + 1] - bounds[i] for i in range(len(keys))], len(flags)


def expected_codecs(path):
    n = path.lower()
    if n.endswith(".av1.mp4"):
        return {"av1"}
    if n.endswith(".webm"):
        return {"vp9", "av1"}
    return {"h264"}


def verify(path, max_mb=6.0, expect_fps=None, expect_gop=None):
    i = V.probe(path)
    fails = []
    want = expected_codecs(path)
    if i["vcodec"] not in want:
        fails.append(f"codec={i['vcodec']}")
    if i["pix_fmt"] != "yuv420p":
        fails.append(f"pix_fmt={i['pix_fmt']}")
    if i["has_audio"]:
        fails.append("audio_stream")
    faststart = None
    if path.lower().endswith(".mp4"):
        atoms = V.mp4_top_atoms(path)
        faststart = ("moov" in atoms and "mdat" in atoms
                     and atoms.index("moov") < atoms.index("mdat"))
        if not faststart:
            fails.append("no_faststart")
    gops, npk = keyframe_intervals(path)
    gop_max = max(gops) if gops else None
    if gop_max is None:
        fails.append("no_keyframes")
    elif expect_gop and gop_max > expect_gop:
        fails.append(f"gop_max={gop_max}>{expect_gop}")
    if expect_fps and abs(i["fps"] - expect_fps) > 0.01:
        fails.append(f"fps={i['fps']:.3f}")
    if i["bytes"] > max_mb * V.MB:
        fails.append(f"bytes>{max_mb}MB")
    return {"path": path, "verdict": "FAIL" if fails else "PASS", "fails": fails,
            "codec": i["vcodec"], "pix_fmt": i["pix_fmt"], "audio": i["has_audio"],
            "faststart": faststart, "gop_max": gop_max, "keyframes": len(gops),
            "frames": npk, "fps": round(i["fps"], 3), "bytes": i["bytes"],
            "duration": round(i["duration"], 3), "size": f"{i['width']}x{i['height']}"}


def collect(items):
    out = []
    for it in items:
        if os.path.isdir(it):
            out += sorted(os.path.join(it, f) for f in os.listdir(it)
                          if f.lower().endswith((".mp4", ".webm")))
        else:
            out.append(V.need(it))
    return out


def selftest():
    d = V.selftest_dir("verify_web_media")
    try:
        import web_normalize as WN
        raw = V.lavfi_clip(os.path.join(d, "raw.mp4"), duration=2.0, audio=True)
        good = os.path.join(d, "good.mp4")
        WN.normalize(raw, good, fps=24, gop=8, preset="veryfast")
        rg = verify(good, 6, 24, 8)
        # positive control 1: a clip WITH audio must FAIL (and lavfi_clip's raw output also
        # lacks faststart and has a long GOP)
        withaudio = os.path.join(d, "withaudio.mp4")
        V.ff(["-i", good, "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-map", "0:v",
              "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags",
              "+faststart", withaudio])
        ra = verify(withaudio, 6, 24, 8)
        # positive control 2: no faststart (moov after mdat) must FAIL on that check alone
        nofs = os.path.join(d, "nofs.mp4")
        V.ff(["-i", good, "-c", "copy", nofs])
        rn = verify(nofs, 6, 24, 8)
        # positive control 3: long GOP must FAIL
        rl = verify(raw, 6, 24, 8)
        ok = (rg["verdict"] == "PASS" and ra["verdict"] == "FAIL" and "audio_stream" in ra["fails"]
              and rn["fails"] == ["no_faststart"] and any(f.startswith("gop_max") for f in rl["fails"]))
        print(f"selftest verify_web_media: normalized={rg['verdict']} gop_max={rg['gop_max']} "
              f"faststart={int(bool(rg['faststart']))} | control_audio={ra['verdict']} "
              f"fails={len(ra['fails'])} | control_no_faststart={rn['verdict']} | "
              f"control_raw_long_gop={rl['verdict']} gop_max={rl['gop_max']} "
              f"-> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        V.selftest_cleanup(d)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items", nargs="*", help="files and/or directories")
    ap.add_argument("--max-mb", type=float, default=6.0)
    ap.add_argument("--expect-fps", type=float)
    ap.add_argument("--expect-gop", type=int)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    files = collect(a.items) if a.items else []
    if not files:
        ap.print_usage(sys.stderr); return 2
    bad = []
    for f in files:
        r = verify(f, a.max_mb, a.expect_fps, a.expect_gop)
        print(f"{r['verdict']}  {r['path']}  {r['codec']} {r['pix_fmt']} {r['size']} "
              f"fps={r['fps']} gop_max={r['gop_max']} keyframes={r['keyframes']} "
              f"frames={r['frames']} bytes={r['bytes']} duration={r['duration']} "
              f"audio={int(r['audio'])} faststart={r['faststart']}")
        if r["fails"]:
            bad.append((f, r["fails"]))
    print(f"files={len(files)} pass={len(files) - len(bad)} fail={len(bad)}")
    for f, why in bad:
        print(f"FAIL {f}: {','.join(why)}")
    return 1 if bad else 0


if __name__ == "__main__":
    V.main_guard(main)
