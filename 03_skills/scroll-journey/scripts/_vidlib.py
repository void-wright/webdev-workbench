#!/usr/bin/env python3
"""
Shared helpers for the scroll-journey web-passage tools (boundary_frames, seam_check,
color_match, web_normalize, seam_repair, route_sheet, verify_web_media, loop_seal and the
detectors).

CPU ONLY. Everything here is ffmpeg/ffprobe + numpy/Pillow. Nothing in this toolkit needs or
uses a GPU.

The normalisation recipe follows the upstream sn-motion-html method (MIT; see VENDOR_NOTE.md):
cover-scale + centre crop, constant fps, libx264 yuv420p, short fixed GOP with no scene-cut
keyframes, -an, +faststart. Boundary frames: select=eq(n\\,0) for the first; an -sseof seek
for the last, hardened here so the last frame is the TRUE last frame even on very short clips.

Scratch: temporary files go under $SCROLL_JOURNEY_SCRATCH (default ~/.cache/scroll-journey),
never /tmp. Requires ffmpeg 5.1 or newer (the last-frame read uses -fps_mode).

Not a CLI. Imported by the sibling scripts (run them with `python3 -B`).
"""
import os
import sys

sys.dont_write_bytecode = True

import json
import re
import shutil
import subprocess
from fractions import Fraction

FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",       # Debian, Ubuntu
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono-Bold.ttf",  # Fedora
    "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",        # macOS
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",
)
MB = 1_000_000            # budgets are decimal megabytes: --max-mb 6 means 6,000,000 bytes


def scratch_root():
    """Where every temporary file goes: $SCROLL_JOURNEY_SCRATCH, else ~/.cache/scroll-journey."""
    d = os.environ.get("SCROLL_JOURNEY_SCRATCH") or os.path.join(
        os.path.expanduser("~"), ".cache", "scroll-journey")
    os.makedirs(d, exist_ok=True)
    return d


def font_path():
    """A TrueType font for labels, or None (callers then use Pillow's built-in font)."""
    return next((f for f in FONT_CANDIDATES if os.path.isfile(f)), None)


def pil_font(size=16):
    from PIL import ImageFont
    f = font_path()
    if f:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)     # Pillow 10.1+
    except TypeError:
        return ImageFont.load_default()


def has_encoder(name):
    """True when this ffmpeg build carries the named encoder (e.g. libsvtav1, libvpx-vp9)."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return any(ln.split()[1:2] == [name] for ln in p.stdout.splitlines() if ln.strip())


class ToolError(Exception):
    """A usage-level problem (missing file, bad argument) -> exit 2."""


def run(cmd, check=True):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        tail = (p.stderr or "").strip().splitlines()[-3:]
        raise RuntimeError(f"command failed rc={p.returncode}: {cmd[0]} :: " + " | ".join(tail))
    return p


def ff(args, level="error", check=True):
    """ffmpeg with -nostdin -y. `level` controls what lands on stderr (parsers want 'info')."""
    return run(["ffmpeg", "-hide_banner", "-nostdin", "-v", level, "-y"] + list(args), check=check)


def need(path):
    if not os.path.isfile(path):
        raise ToolError(f"missing file: {path}")
    return path


def probe(path):
    """Video facts from ffprobe. nb_frames is COUNTED (packets), not trusted from the header."""
    need(path)
    p = run(["ffprobe", "-v", "error", "-count_packets", "-show_entries",
             "stream=index,codec_type,codec_name,pix_fmt,width,height,r_frame_rate,"
             "avg_frame_rate,nb_read_packets:format=duration,size,format_name",
             "-of", "json", path])
    d = json.loads(p.stdout)
    streams = d.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    if v is None:
        raise ToolError(f"no video stream: {path}")
    rate = v.get("avg_frame_rate") or "0/1"
    if rate in ("0/0", "0/1"):
        rate = v.get("r_frame_rate") or "0/1"
    fps = float(Fraction(rate)) if rate not in ("0/0",) else 0.0
    fmt = d.get("format", {})
    return {
        "path": path,
        "vcodec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"),
        "width": int(v.get("width", 0)),
        "height": int(v.get("height", 0)),
        "fps": fps,
        "fps_str": rate,
        "frames": int(v.get("nb_read_packets") or 0),
        "duration": float(fmt.get("duration") or 0.0),
        "bytes": int(fmt.get("size") or os.path.getsize(path)),
        "has_audio": any(s.get("codec_type") == "audio" for s in streams),
        "format_name": fmt.get("format_name", ""),
    }


def first_frame(clip, out_png):
    ff(["-i", need(clip), "-vf", r"select=eq(n\,0)", "-frames:v", "1", out_png])
    return out_png


def last_frame(clip, out_png):
    """True last frame. Seek to (at most) 1 s before EOF and let -update 1 overwrite the PNG
    with every decoded frame, so what remains is the final frame. Unlike a bare
    `-sseof -0.05 -frames:v 1`, this cannot land one frame early on a seek snap, and on a
    clip shorter than the seek window it simply decodes from the start."""
    info = probe(clip)
    back = min(1.0, max(info["duration"], 0.05))
    ff(["-sseof", f"-{back:.3f}", "-i", clip, "-update", "1", "-fps_mode", "passthrough", out_png])
    if not os.path.isfile(out_png):
        raise RuntimeError("last frame not written")
    return out_png


def cover_filter(w, h, crop_y=None):
    """Scale-to-cover then crop to exactly w x h. crop_y = 0..1 picks the vertical crop
    position (0 top, 0.5 centre, 1 bottom); None = centre."""
    s = f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos"
    if crop_y is None:
        return f"{s},crop={w}:{h}"
    return f"{s},crop={w}:{h}:(iw-{w})/2:(ih-{h})*{float(crop_y):.4f}"


def ssim_images(a, b, w=None, h=None):
    """SSIM (ffmpeg ssim filter, 'All') of image/video-frame a vs b. b is cover-scaled to a's
    size (or w x h); both converted to yuv420p so the pixel format is identical."""
    if w is None or h is None:
        i = probe(a)
        w, h = i["width"], i["height"]
    g = (f"[0:v]{cover_filter(w, h)},format=yuv420p[a];"
         f"[1:v]{cover_filter(w, h)},format=yuv420p[b];[a][b]ssim")
    p = ff(["-i", need(a), "-i", need(b), "-lavfi", g, "-frames:v", "1", "-f", "null", "-"],
           level="info")
    m = re.findall(r"All:([0-9.]+)", p.stderr)
    if not m:
        raise RuntimeError("ssim not parsed")
    return float(m[-1])


def ssim_series(clip, still, workdir):
    """Per-frame SSIM of every clip frame vs one still -> list[float] indexed by frame."""
    info = probe(clip)
    w, h = info["width"], info["height"]
    stats = os.path.join(workdir, "_ssim_series.log")
    g = (f"[0:v]format=yuv420p[c];[1:v]{cover_filter(w, h)},format=yuv420p[s];"
         f"[c][s]ssim=stats_file={stats}:shortest=1")
    ff(["-i", clip, "-loop", "1", "-i", need(still), "-lavfi", g, "-f", "null", "-"])
    vals = []
    with open(stats) as fh:
        for line in fh:
            m = re.search(r"All:([0-9.]+)", line)
            if m:
                vals.append(float(m.group(1)))
    os.remove(stats)
    return vals


def adjacent_ssim(clip, workdir):
    """SSIM of every frame vs the next one -> (median, min). The clip's own frame-step
    baseline: a seam is invisible when it is no worse than an ordinary step."""
    import statistics
    stats = os.path.join(workdir, "_adj_ssim.log")
    ff(["-i", need(clip), "-i", clip, "-lavfi",
        f"[1:v]trim=start_frame=1,setpts=PTS-STARTPTS[b];[0:v][b]ssim=stats_file={stats}:shortest=1",
        "-f", "null", "-"])
    with open(stats) as fh:
        v = [float(m) for m in re.findall(r"All:([0-9.]+)", fh.read())]
    os.remove(stats)
    if not v:
        raise RuntimeError("adjacent ssim not parsed")
    return statistics.median(v), min(v)


def rgb_array(path, w=None, h=None, max_frames=None, fps_sample=None):
    """Decode to an (n, h, w, 3) uint8 numpy array via rawvideo rgb24 (downscaled)."""
    import numpy as np
    info = probe(path)
    W = w or min(320, info["width"])
    H = h or max(2, int(round(info["height"] * W / max(info["width"], 1) / 2)) * 2)
    vf = f"scale={W}:{H}:flags=area,format=rgb24"
    if fps_sample:
        vf = f"fps={fps_sample}," + vf
    args = ["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-i", path, "-vf", vf]
    if max_frames:
        args += ["-frames:v", str(max_frames)]
    args += ["-f", "rawvideo", "-"]
    p = subprocess.run(args, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("decode failed")
    n = len(p.stdout) // (W * H * 3)
    return np.frombuffer(p.stdout, dtype=np.uint8)[: n * W * H * 3].reshape(n, H, W, 3)


def channel_stats(path, **kw):
    """Per-channel (R,G,B) mean and std over all decoded pixels."""
    a = rgb_array(path, **kw).astype("float64")
    flat = a.reshape(-1, 3)
    return flat.mean(axis=0).tolist(), flat.std(axis=0).tolist()


def mp4_top_atoms(path):
    """Top-level ISO-BMFF atom types in file order (for the faststart moov-before-mdat check)."""
    atoms = []
    size_total = os.path.getsize(path)
    with open(path, "rb") as fh:
        pos = 0
        while pos + 8 <= size_total and len(atoms) < 64:
            fh.seek(pos)
            hdr = fh.read(8)
            size = int.from_bytes(hdr[:4], "big")
            typ = hdr[4:8].decode("latin-1")
            if size == 1:
                size = int.from_bytes(fh.read(8), "big")
            elif size == 0:
                size = size_total - pos
            if size < 8:
                break
            atoms.append(typ)
            pos += size
    return atoms


def selftest_dir(tool):
    d = os.path.join(scratch_root(), f"selftest_{os.getpid()}", tool)
    os.makedirs(d, exist_ok=True)
    return d


def selftest_cleanup(d):
    root = os.path.dirname(d)
    shutil.rmtree(d, ignore_errors=True)
    try:
        os.rmdir(root)            # only if empty: another tool's selftest may share the pid dir
    except OSError:
        pass


def _src(src, opts):
    """'testsrc2' -> 'testsrc2=opts'; 'color=c=red' -> 'color=c=red:opts'."""
    return f"{src}:{opts}" if "=" in src else f"{src}={opts}"


def lavfi_clip(out, src="testsrc2", size="640x360", rate=24, duration=3.0, audio=False,
               crf=18, extra_vf=None):
    """Synthetic H.264 test clip from a lavfi source. Not web-normalised on purpose."""
    vf = "format=yuv420p" if not extra_vf else f"{extra_vf},format=yuv420p"
    args = ["-f", "lavfi", "-i", _src(src, f"size={size}:rate={rate}:duration={duration}")]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}"]
    args += ["-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf)]
    args += (["-c:a", "aac", "-shortest"] if audio else ["-an"])
    ff(args + [out])
    return out


def lavfi_still(out, src="testsrc2", size="640x360", t=0.0, rate=24, extra_vf=None):
    """One PNG frame of a lavfi source at time t (lossless, for seam references).
    extra_vf is applied BEFORE the frame select, exactly as lavfi_clip applies it."""
    # select by FRAME INDEX: a rounded time string (e.g. 70/24 -> "2.9167") can select the
    # next frame instead, so two different t values may silently return the same frame
    sel = r"select=eq(n\," + str(int(round(t * rate))) + ")"
    ff(["-f", "lavfi", "-i", _src(src, f"size={size}:rate={rate}:duration={t + 1.0}"),
        "-vf", f"{extra_vf},{sel}" if extra_vf else sel, "-frames:v", "1", out])
    return out


def emit(obj):
    print(json.dumps(obj, indent=1, sort_keys=False))


def main_guard(fn):
    """Run fn() -> int, mapping ToolError to exit 2 and anything else to exit 1."""
    try:
        rc = fn()
    except ToolError as e:
        print(f"usage error: {e}", file=sys.stderr)
        rc = 2
    except RuntimeError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        rc = 1
    sys.exit(int(rc or 0))


def paper_stats(path, fps_sample=4, w=160, ring=0.04):
    """WHITE-GROUND check (page journeys on white paper): is the clip's paper the page's #FFF?
    Per sampled frame: p95 luminance (the paper's level), the tint of the brightest decile
    (max - min of its mean R, G, B: a grey veil reads neutral, a cast reads tinted), and the mean
    luminance of the outer `ring` of the frame (where the clip meets the page). Returns the worst
    frame of each and the paper's per-channel white level (median over frames of each channel's
    99th percentile), which --paper-lift maps to 255."""
    import numpy as np
    a = rgb_array(path, w=w, fps_sample=fps_sample).astype("float64")
    if not len(a):
        raise RuntimeError("no frames decoded")
    n, H, W, _ = a.shape
    lum = a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722
    p95, tint, ringm, white = [], [], [], []
    bh, bw = max(1, int(H * ring)), max(1, int(W * ring))
    for i in range(n):
        L = lum[i]
        p95.append(float(np.percentile(L, 95)))
        m = L >= np.percentile(L, 90)
        mean = a[i][m].mean(axis=0)
        tint.append(float(mean.max() - mean.min()))
        rmask = np.zeros((H, W), bool)
        rmask[:bh, :] = rmask[-bh:, :] = True
        rmask[:, :bw] = rmask[:, -bw:] = True
        ringm.append(float(L[rmask].mean()))
        white.append([float(np.percentile(a[i][..., c], 99)) for c in range(3)])
    white = np.median(np.array(white), axis=0).tolist()
    return {"frames": n,
            "paper_p95_min": round(min(p95), 2), "paper_p95_frame": int(np.argmin(p95)),
            "paper_tint_max": round(max(tint), 2), "paper_tint_frame": int(np.argmax(tint)),
            "ring_mean_min": round(min(ringm), 2),
            "white_rgb": [round(x, 2) for x in white]}
