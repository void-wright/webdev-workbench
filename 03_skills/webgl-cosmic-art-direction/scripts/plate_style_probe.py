#!/usr/bin/env python3
"""plate_style_probe.py: measure the cosmic style of any image (a painted plate or a screenshot of your own figure).

Prints the dark→light palette bands of the cloud field and the mean radial luminance profile of the
brightest stars (half-max and 10% radii), so a rendered star can be compared with a painted one.
CPU only; no model loaded.

  python3 plate_style_probe.py IMAGE [--scale-to 1376] [--top 12] [--region x0,y0,x1,y1]
  python3 plate_style_probe.py IMAGE --thread x0,y0,x1,y1     # cross-section of one thread segment
"""
import argparse
import numpy as np
from PIL import Image
from scipy.ndimage import maximum_filter, map_coordinates

ap = argparse.ArgumentParser()
ap.add_argument('image')
ap.add_argument('--scale-to', type=int, default=0, help='report radii as if the image were this many px wide')
ap.add_argument('--top', type=int, default=12)
ap.add_argument('--region', default='')
ap.add_argument('--thread', action='append', default=[])
a_ = ap.parse_args()

img = np.asarray(Image.open(a_.image).convert('RGB')).astype(float)
if a_.region:
    x0, y0, x1, y1 = map(int, a_.region.split(','))
    img = img[y0:y1, x0:x1]
h, w, _ = img.shape
lum = img @ [0.2126, 0.7152, 0.0722]
hx = lambda c: '#%02x%02x%02x' % tuple(int(round(v)) for v in c)
k = (a_.scale_to / w) if a_.scale_to else 1.0

q = np.percentile(lum, [5, 25, 50, 75, 95])
bands = [(-1, q[0]), (q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[4])]
print(f'{a_.image} {w}x{h}' + (f' (radii scaled to {a_.scale_to}px wide)' if a_.scale_to else ''))
print('  cloud bands dark→light', [hx(img[(lum > lo) & (lum <= hi)].mean(0)) for lo, hi in bands])

thr = np.percentile(lum, 99.85)
mx = (lum == maximum_filter(lum, 9)) & (lum > thr)
ys, xs = np.nonzero(mx)
R = 12
prof, cores = [], []
for i in np.argsort(-lum[ys, xs])[: a_.top]:
    y, x = ys[i], xs[i]
    if y < R or x < R or y > h - R - 1 or x > w - R - 1:
        continue
    patch = lum[y - R:y + R + 1, x - R:x + R + 1]
    yy, xx = np.mgrid[-R:R + 1, -R:R + 1]
    r = np.hypot(yy, xx)
    prof.append([patch[(r >= j - .5) & (r < j + .5)].mean() for j in range(R)])
    cores.append(img[y - 1:y + 2, x - 1:x + 2].reshape(-1, 3).mean(0))
if prof:
    p = np.array(prof).mean(0)
    bg, pk = p[-1], p[0]
    half = next(j for j in range(R) if p[j] - bg < .5 * (pk - bg))
    tenth = next((j for j in range(R) if p[j] - bg < .1 * (pk - bg)), R)
    print(f'  stars n={len(prof)} core {hx(np.mean(cores, 0))} profile {[int(v) for v in p]}')
    print(f'  half-max r≈{half * k:.1f}px  10% r≈{tenth * k:.1f}px')

for t in a_.thread:
    x0, y0, x1, y1 = map(float, t.split(','))
    P, Q = np.array([x0, y0]), np.array([x1, y1])
    d = (Q - P) / np.linalg.norm(Q - P)
    n = np.array([-d[1], d[0]])
    offs = np.arange(-10, 10.5, .5)
    rows = []
    for s in np.linspace(.3, .7, 9):
        c = P + (Q - P) * s
        pts = c[None, :] + offs[:, None] * n[None, :]
        pr = map_coordinates(lum, [pts[:, 1], pts[:, 0]], order=1)
        rows.append((np.roll(pr, 20 - int(np.argmax(pr))), c + offs[int(np.argmax(pr))] * n, offs[int(np.argmax(pr))]))
    pr = np.mean([r[0] for r in rows], 0)
    base = np.median(np.r_[pr[:6], pr[-6:]])
    pk = pr.max()
    fw = np.nonzero(pr - base > .5 * (pk - base))[0]
    w15 = np.nonzero(pr - base > .15 * (pk - base))[0]
    col = [np.mean([map_coordinates(img[..., ch], [[r[1][1]], [r[1][0]]], order=1)[0] for r in rows]) for ch in range(3)]
    spread = np.std([r[2] for r in rows])
    print(f'  thread {t}: ridge {pk:.0f} over {base:.0f}; FWHM≈{(fw[-1] - fw[0] + 1) * .5 * k:.1f}px '
          f'15%-width≈{(w15[-1] - w15[0] + 1) * .5 * k:.1f}px colour {hx(col)} ridge-spread {spread:.2f}px'
          + ('  (UNRELIABLE: ridge wanders, not one thread)' if spread > 1.5 else ''))
