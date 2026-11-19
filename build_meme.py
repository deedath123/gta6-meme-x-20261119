#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme: composite the official make.fun ghost mascot
(extracted from the press-kit mark) into the generated Vice City launch-queue
scene as a character in the queue, then add meme captions."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

WORK = "/home/hatch/workspace/makefun/gta6memework"
scene = Image.open(f"{WORK}/scene-base.png").convert("RGB")  # 1600x1600
mark = Image.open(f"{WORK}/ghost-mark.png").convert("RGBA")  # 1024x1024
a = np.array(mark)
rgb, alpha = a[:, :, :3].astype(int), a[:, :, 3]

# --- extract ghost body: largest near-white connected component ---
white = (rgb[:, :, 0] > 240) & (rgb[:, :, 1] > 240) & (rgb[:, :, 2] > 240) & (alpha > 200)
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n + 1))
ghost_id = 1 + int(np.argmax(sizes))
ghost = lab == ghost_id
print("ghost body px:", int(ghost.sum()))

# --- the star coin: white star component on the right side of the badge ---
comps = []
for i in range(1, n + 1):
    if i == ghost_id:
        continue
    ys, xs = np.where(lab == i)
    if len(xs) > 200:  # the star is a few hundred px
        comps.append((len(xs), xs.mean(), ys.mean()))
comps.sort(reverse=True)
# comps holds the star (centroid ~772,446) and the plain white circle (~735,591);
# the coin is centred on the STAR, i.e. the component with the higher centroid.
_, star_x, star_y = min(comps, key=lambda c: c[2])
print("star centroid:", star_x, star_y)
coin_cx, coin_cy, coin_r = int(star_x), int(star_y), 118
yy, xx = np.mgrid[0:1024, 0:1024]
coin = (xx - coin_cx) ** 2 + (yy - coin_cy) ** 2 <= coin_r ** 2

# --- sprite mask: ghost body dilated to include its black outline, plus coin ---
ghost_d = ndimage.binary_dilation(ghost, iterations=12)
mask = (ghost_d | coin) & (alpha > 0)
ys, xs = np.where(mask)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
print("sprite bbox:", x0, y0, x1, y1)
sprite = Image.fromarray(a).crop((x0, y0, x1, y1))
smask = Image.fromarray((mask[y0:y1, x0:x1] * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(1.2)
)
sprite.putalpha(smask)

# --- place the ghost in the queue, foreground left ---
target_h = 740
scale = target_h / sprite.height
sprite = sprite.resize((int(sprite.width * scale), target_h), Image.LANCZOS)
px, py = 60, 660  # feet at y = 1400
shadow = Image.new("RGBA", scene.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sw = int(sprite.width * 0.62)
sd.ellipse([px + sprite.width // 2 - sw // 2, py + target_h - 26,
            px + sprite.width // 2 + sw // 2, py + target_h + 22], fill=(0, 0, 0, 110))
scene = Image.alpha_composite(scene.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(10)))
scene.alpha_composite(sprite, (px, py))

# --- captions: bold white with heavy black stroke, classic meme style ---
d = ImageDraw.Draw(scene)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def caption(text, size, cy):
    f = ImageFont.truetype(FONT, size)
    while d.textlength(text, font=f) > 1520 and size > 30:
        size -= 4
        f = ImageFont.truetype(FONT, size)
    w = d.textlength(text, font=f)
    d.text(((1600 - w) / 2, cy), text, font=f, fill=(255, 255, 255),
           stroke_width=max(4, size // 11), stroke_fill=(0, 0, 0))

caption("2013: QUEUED FOR GTA V AT 13", 96, 46)
caption("2026: QUEUED FOR GTA 6 — AS THE DAD", 84, 1478)

out = scene.convert("RGB")
out.save(f"{WORK}/meme.png")
out.resize((480, 480)).save(f"{WORK}/meme-480.png")
print("saved meme.png", out.size)
