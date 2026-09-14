"""Renders icon.tga and the CurseForge avatar. Needs Pillow.

A gold ankh, the life symbol, on deep teal with rays behind it.
"""

from PIL import Image, ImageDraw, ImageFilter
import math
IRON = (74, 74, 88)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

class Ctx:
    def __init__(self, N, S=8, pad=0.47):
        self.N, self.S, self.pad = N, S, pad
        self.P = N * S
        self.c = self.P / 2
        self.img = self.canvas()
    def canvas(self):
        return Image.new("RGBA", (self.P, self.P), (0, 0, 0, 0))
    def bg(self, mid, deep, power=0.8):
        d = ImageDraw.Draw(self.img); c, P = self.c, self.P
        for i in range(200, 0, -1):
            t = i / 200; r = P * self.pad * t
            d.ellipse([c - r, c - r, c + r, c + r], fill=lerp(mid, deep, t ** power) + (255,))
    def glow(self, fn, blur, alpha):
        g = self.canvas(); fn(ImageDraw.Draw(g))
        g = g.filter(ImageFilter.GaussianBlur(blur))
        g.putalpha(g.split()[3].point(lambda v: int(v * alpha)))
        self.img.alpha_composite(g)
    def clip(self, img, r=None):
        r = r or self.P * self.pad * 0.955; c, P = self.c, self.P
        m = Image.new("L", (P, P), 0)
        ImageDraw.Draw(m).ellipse([c - r, c - r, c + r, c + r], fill=255)
        img.putalpha(Image.composite(img.split()[3], Image.new("L", (P, P), 0), m))
        return img
    def bezel(self, col=IRON):
        d = ImageDraw.Draw(self.img); c, P, pad = self.c, self.P, self.pad
        d.ellipse([c - P * pad, c - P * pad, c + P * pad, c + P * pad], outline=col + (255,), width=int(P * 0.034))
        r = P * pad * 0.962
        d.ellipse([c - r, c - r, c + r, c + r], outline=lerp(col, (0, 0, 0), 0.55) + (210,), width=int(P * 0.013))
    def out(self):
        return self.img.resize((self.N, self.N), Image.LANCZOS)

def skull(d, cx, cy, r, col, dark):
    # cranium
    d.ellipse([cx - r, cy - r * 1.05, cx + r, cy + r * 0.55], fill=col)
    # jaw
    d.rounded_rectangle([cx - r * 0.62, cy + r * 0.1, cx + r * 0.62, cy + r * 0.95], radius=r * 0.22, fill=col)
    # cheek notches
    d.polygon([(cx - r, cy + r * 0.25), (cx - r * 0.62, cy + r * 0.25), (cx - r * 0.62, cy + r * 0.7)], fill=dark)
    d.polygon([(cx + r, cy + r * 0.25), (cx + r * 0.62, cy + r * 0.25), (cx + r * 0.62, cy + r * 0.7)], fill=dark)
    # eyes
    er = r * 0.3
    for ex in (cx - r * 0.42, cx + r * 0.42):
        d.ellipse([ex - er, cy - r * 0.35 - er * 0.9, ex + er, cy - r * 0.35 + er * 0.9], fill=dark)
    # nose
    d.polygon([(cx, cy + r * 0.05), (cx - r * 0.14, cy + r * 0.35), (cx + r * 0.14, cy + r * 0.35)], fill=dark)
    # teeth lines
    for tx in (-0.3, -0.1, 0.1, 0.3):
        d.rectangle([cx + r * tx - r * 0.025, cy + r * 0.6, cx + r * tx + r * 0.025, cy + r * 0.95], fill=dark)

def render(N, S=8):
    x = Ctx(N, S)
    c, P = x.c, x.P
    x.bg((10, 66, 70), (3, 10, 12))
    GOLD, GOLD_HI, GOLD_LO = (244, 196, 70), (255, 246, 205), (120, 82, 18)
    w = P * 0.11
    def ankh(g, col, width, off=(0, 0)):
        ox, oy = off
        # loop
        g.ellipse([c - P * 0.17 + ox, c - P * 0.42 + oy, c + P * 0.17 + ox, c - P * 0.06 + oy], outline=col, width=int(width))
        # stem
        g.rounded_rectangle([c - width / 2 + ox, c - P * 0.10 + oy, c + width / 2 + ox, c + P * 0.42 + oy], radius=width * 0.3, fill=col)
        # arms
        g.rounded_rectangle([c - P * 0.30 + ox, c - P * 0.05 - width / 2 + oy, c + P * 0.30 + ox, c - P * 0.05 + width / 2 + oy], radius=width * 0.3, fill=col)
    x.glow(lambda g: ankh(g, GOLD_HI + (255,), w * 1.5), P * 0.05, 0.9)
    # radiating light
    rays = x.canvas(); rd = ImageDraw.Draw(rays)
    for i in range(12):
        a = i * math.pi / 6 + math.pi / 12
        rd.polygon([(c, c), (c + P * 0.6 * math.cos(a - 0.09), c + P * 0.6 * math.sin(a - 0.09)), (c + P * 0.6 * math.cos(a + 0.09), c + P * 0.6 * math.sin(a + 0.09))], fill=(255, 240, 180, 60))
    x.img.alpha_composite(x.clip(rays.filter(ImageFilter.GaussianBlur(P * 0.02))))
    d = ImageDraw.Draw(x.img)
    ankh(d, (0, 0, 0, 170), w, (0, P * 0.03))
    ankh(d, GOLD_LO + (255,), w)
    ankh(d, GOLD + (255,), w * 0.62, (0, -w * 0.12))
    ankh(d, GOLD_HI + (255,), w * 0.2, (0, -w * 0.28))
    x.bezel(); return x.out()


icon = render(128)
icon.save("images/icon-128.png")
icon.save("icon.tga", compression=None)
render(512, S=4).save("images/curseforge-avatar.png")
print("ok")
