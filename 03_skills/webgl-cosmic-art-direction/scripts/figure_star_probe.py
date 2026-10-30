"""Radial luminance profile of named figure stars in a stage screenshot, radii reported at plate scale (1376 px)."""
import json, sys, numpy as np
from PIL import Image
shot, layout_json, which = sys.argv[1], sys.argv[2], sys.argv[3]
ids = sys.argv[4].split(',')
img = np.asarray(Image.open(shot).convert('RGB')).astype(float); lum = img @ [0.2126, 0.7152, 0.0722]
h, w = lum.shape
L = json.load(open(layout_json))[which]; VW, VH = L['viewBox']; sx = w / VW
k = 1376 / w
R = 40
for s in L['stars']:
    if s['id'] not in ids: continue
    x, y = s['x'] * sx, s['y'] * sx
    yy, xx = np.mgrid[0:h, 0:w]; r = np.hypot(yy - y, xx - x)
    prof = np.array([lum[(r >= j - .5) & (r < j + .5)].mean() for j in range(R)])
    bg, pk = prof[-1], prof[0]
    half = next(j for j in range(R) if prof[j] - bg < .5 * (pk - bg))
    tenth = next((j for j in range(R) if prof[j] - bg < .1 * (pk - bg)), R)
    print(f"{s['id']:12s} mag {s['mag']:.2f}: peak {pk:.0f} bg {bg:.0f}  half-max r≈{half*k:.1f}px  10% r≈{tenth*k:.1f}px  (plate scale; stage {w}px)  profile@plate {[int(v) for v in prof[:int(14/k)+1:max(1,int(round(1/k)))]]}")
