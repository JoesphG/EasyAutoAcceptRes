"""Renders icon.tga and the CurseForge avatar. Needs Pillow.

A gold tick in a column of holy light: the resurrection accepted for you.
"""

from PIL import Image, ImageDraw, ImageFilter

BG_MID = (44, 30, 84)
BG_DEEP = (8, 6, 16)
IRON = (74, 74, 88)
LIGHT = (255, 236, 170)
GOLD = (244, 190, 64)
GOLD_HI = (255, 244, 196)
GOLD_LO = (120, 78, 18)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def render(N, S=8, pad=0.47):
    P = N * S
    c = P / 2

    def canvas():
        return Image.new("RGBA", (P, P), (0, 0, 0, 0))

    def glow(fn, blur, alpha):
        g = canvas()
        fn(ImageDraw.Draw(g))
        g = g.filter(ImageFilter.GaussianBlur(blur))
        g.putalpha(g.split()[3].point(lambda v: int(v * alpha)))
        return g

    def clip_circle(img, r):
        m = Image.new("L", (P, P), 0)
        ImageDraw.Draw(m).ellipse([c - r, c - r, c + r, c + r], fill=255)
        img.putalpha(Image.composite(img.split()[3], Image.new("L", (P, P), 0), m))
        return img

    img = canvas()
    d = ImageDraw.Draw(img)
    for i in range(200, 0, -1):
        t = i / 200
        r = P * pad * t
        d.ellipse([c - r, c - r, c + r, c + r], fill=lerp(BG_MID, BG_DEEP, t**0.8) + (255,))

    # column of light, widening as it rises
    beam = canvas()
    bd = ImageDraw.Draw(beam)
    top, bot = P * 0.04, P * 0.96
    for i in range(60):
        t = i / 60
        y = top + (bot - top) * t
        w = P * (0.30 - 0.22 * t)
        a = int(150 * (1 - abs(t - 0.45) * 1.6))
        bd.rectangle([c - w, y, c + w, y + (bot - top) / 60 + 1], fill=LIGHT + (max(a, 0),))
    beam = beam.filter(ImageFilter.GaussianBlur(P * 0.05))
    img.alpha_composite(clip_circle(beam, P * pad * 0.955))
    img.alpha_composite(
        glow(lambda g: g.ellipse([c - P * 0.2, c - P * 0.2, c + P * 0.2, c + P * 0.2], fill=GOLD + (255,)), P * 0.09, 0.7)
    )

    # tick
    w = P * 0.11
    pts = [(c - P * 0.30, c + P * 0.02), (c - P * 0.09, c + P * 0.24), (c + P * 0.32, c - P * 0.24)]

    def tick(d, off, col, width):
        d.line([(x + off[0], y + off[1]) for x, y in pts], fill=col, width=int(width), joint="curve")
        for x, y in (pts[0], pts[2]):
            d.ellipse([x + off[0] - width / 2, y + off[1] - width / 2, x + off[0] + width / 2, y + off[1] + width / 2], fill=col)

    img.alpha_composite(glow(lambda g: tick(g, (0, 0), GOLD_HI + (255,), w * 1.3), P * 0.035, 0.9))
    d = ImageDraw.Draw(img)
    tick(d, (0, P * 0.03), (0, 0, 0, 160), w)
    tick(d, (0, 0), GOLD_LO + (255,), w)
    tick(d, (0, -w * 0.18), GOLD + (255,), w * 0.72)
    tick(d, (0, -w * 0.30), GOLD_HI + (255,), w * 0.24)

    # bezel
    d.ellipse([c - P * pad, c - P * pad, c + P * pad, c + P * pad], outline=IRON + (255,), width=int(P * 0.034))
    d.ellipse(
        [c - P * pad * 0.962, c - P * pad * 0.962, c + P * pad * 0.962, c + P * pad * 0.962],
        outline=lerp(IRON, (0, 0, 0), 0.55) + (210,),
        width=int(P * 0.013),
    )
    return img.resize((N, N), Image.LANCZOS)


icon = render(128)
icon.save("images/icon-128.png")
icon.save("icon.tga", compression=None)
render(512, S=4).save("images/curseforge-avatar.png")
print("ok")
