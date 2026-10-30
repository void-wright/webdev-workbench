"""Calm a plate where interactive words or stars will sit: inside a rectangle, remove painted
node-stars, glints and constellation lines (anything brighter than the smooth local sky), keep the clouds and the
tiny dim background stars. Never overwrites: writes <out>. Usage: calm_plate.py in out x0 y0 x1 y1"""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import median_filter, label, binary_dilation, gaussian_filter, maximum_filter
src, out = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7])
a = np.asarray(Image.open(src).convert('RGB')).astype(float)
lum = a @ [0.2126, 0.7152, 0.0722]
sky = np.stack([gaussian_filter(median_filter(a[..., c], size=41), 6) for c in range(3)], -1)  # the smooth local sky (clouds), softened so fills leave no disc
skyl = sky @ [0.2126, 0.7152, 0.0722]
resid = lum - skyl
cand = resid > 10                                                               # brighter than the sky around it
lab, n = label(cand)
remove = np.zeros_like(cand)
kept = removed = 0
for i in range(1, n + 1):
    m = lab == i
    ys, xs = np.nonzero(m)
    cy, cx = ys.mean(), xs.mean()
    if not (x0 <= cx <= x1 and y0 <= cy <= y1):
        continue
    area = m.sum(); peak = resid[m].max(); h = np.ptp(ys) + 1; w = np.ptp(xs) + 1
    elongated = max(h, w) >= 3 * max(1, min(h, w)) and max(h, w) >= 8          # a thread or a painted line
    tiny_dim = area <= 6 and peak < 60                                          # a 1-2 px background star: keep
    if tiny_dim and not elongated:
        kept += 1; continue
    remove |= m; removed += 1
mask = binary_dilation(remove, iterations=7)                                    # take each star's whole halo with it
soft = np.clip(gaussian_filter(mask.astype(float), 3.0) * 1.6, 0, 1)                                 # feather the fill's edge
outa = a * (1 - soft[..., None]) + sky * soft[..., None]
# Save at the SOURCE's own encoding so the master keeps its quality (a default/95 save re-encodes
# every pixel to change a few; for JPEG sources use quality=100 and the source's chroma subsampling).
_src = Image.open(src)
_kw = {}
if (_src.format or '').upper() == 'JPEG':
    from PIL import JpegImagePlugin
    _kw = dict(quality=100, subsampling=JpegImagePlugin.get_sampling(_src))
Image.fromarray(np.clip(outa, 0, 255).astype(np.uint8)).save(out, **_kw)
print(f'components in rect: removed {removed}, kept {kept} tiny dim stars; masked px {int(mask.sum())}')
