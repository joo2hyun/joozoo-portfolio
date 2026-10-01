"""Builds the device / print mockups used in the deck (img/mock-*.jpg).

One or two scenes per project; social posts are shown as Instagram screens.
Everything is drawn at 2× and saved at 1×, sized to the card it fills.
Run `python3 mock.py` before `python3 build.py`.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

IMG = "img/"
X = 2  # supersampling
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
INK = (20, 20, 22)
GREY = (142, 142, 147)
IG = [(254, 218, 117), (250, 126, 30), (214, 41, 118), (150, 47, 191), (79, 91, 213)]


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, int(size))


def load(name):
    return Image.open(IMG + name + ".jpg").convert("RGB")


def trim(im, tol=18):
    """Crop the white margin (and soft drop shadow) the source crops carry."""
    g = im.convert("L").point(lambda v: 255 if v < 255 - tol else 0)
    box = g.getbbox()
    return im.crop(box) if box else im


# ── scene helpers ────────────────────────────────────────────────

def scene(w, h, top=(243, 240, 234), bottom=(226, 221, 211)):
    w, h = w * X, h * X
    grad = Image.linear_gradient("L").resize((w, h))
    return Image.composite(Image.new("RGB", (w, h), bottom), Image.new("RGB", (w, h), top), grad)


def shadow(base, mask, pos, blur=28, off=(0, 26), opacity=0.34):
    """Soft drop shadow plus a tight contact shadow under a shape."""
    for b, o, a in ((blur, off, opacity), (blur // 5, (0, off[1] // 5), opacity * 0.8)):
        sh = Image.new("L", base.size, 0)
        sh.paste(mask.point(lambda v: int(v * a)), (pos[0] + o[0] * X, pos[1] + o[1] * X))
        sh = sh.filter(ImageFilter.GaussianBlur(b * X))
        base.paste(Image.new("RGB", base.size, (60, 52, 40)), (0, 0), sh)


def light(im, strength=0.09):
    """Diagonal light fall-off so flat art reads as a lit surface."""
    w, h = im.size
    g = Image.linear_gradient("L").rotate(-35, expand=True).resize((w, h))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(dark, im, g.point(lambda v: int(v * strength)))


def rounded(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def fit_cover(im, size):
    w, h = size
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def fit_width(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def save(canvas, name):
    canvas = canvas.resize((canvas.width // X, canvas.height // X), Image.LANCZOS)
    canvas.save(IMG + name + ".jpg", quality=88, optimize=True, progressive=True)
    print(name, canvas.size)


def paste_object(base, obj, mask, pos, **kw):
    shadow(base, mask, pos, **kw)
    base.paste(obj, pos, mask)


# ── Instagram ────────────────────────────────────────────────────

def ig_ring(d, box, width):
    """Instagram story ring: a gradient-ish ring drawn as stacked arcs."""
    x0, y0, x1, y1 = box
    for i, c in enumerate(IG):
        d.arc(box, 135 + i * 72, 135 + (i + 1) * 72 + 2, fill=c, width=width)


def avatar(screen, d, cx, cy, r, label):
    ig_ring(d, (cx - r, cy - r, cx + r, cy + r), max(2, r // 7))
    ir = int(r * 0.78)
    d.ellipse((cx - ir, cy - ir, cx + ir, cy + ir), fill=INK)
    f = font(ir * 0.8, True)
    d.text((cx, cy), label, font=f, fill="white", anchor="mm")


def heart(d, x, y, s, fill=None, outline=INK, w=2):
    d.polygon([(x + s * .5, y + s * .92), (x + s * .04, y + s * .45), (x + s * .5, y + s * .25),
               (x + s * .96, y + s * .45)], fill=fill)
    for cx in (x + s * .28, x + s * .72):
        d.ellipse((cx - s * .26, y + s * .06, cx + s * .26, y + s * .56), fill=fill, outline=None)
    if fill is None:
        d.arc((x + s * .02, y + s * .06, x + s * .54, y + s * .58), 140, 360, fill=outline, width=w)
        d.arc((x + s * .46, y + s * .06, x + s * .98, y + s * .58), 180, 40, fill=outline, width=w)
        d.line([(x + s * .07, y + s * .5), (x + s * .5, y + s * .93), (x + s * .93, y + s * .5)],
               fill=outline, width=w, joint="curve")


def icons_row(d, x, y, s, w, color=INK):
    lw = max(2, int(s * .09))
    heart(d, x, y, s, outline=color, w=lw)
    d.ellipse((x + s * 1.55, y + s * .05, x + s * 2.45, y + s * .95), outline=color, width=lw)
    d.polygon([(x + s * 2.95, y + s * .1), (x + s * 3.95, y + s * .1), (x + s * 3.35, y + s * .95)],
              outline=color, width=lw)
    bx = x + w - s * .9
    d.polygon([(bx, y), (bx + s * .7, y), (bx + s * .7, y + s), (bx + s * .35, y + s * .7), (bx, y + s)],
              outline=color, width=lw)


def status_bar(d, sw, s, color=INK):
    d.text((s * 1.6, s * .95), "9:41", font=font(s * .78, True), fill=color, anchor="lm")
    bx = sw - s * 2.6
    d.rounded_rectangle((bx, s * .66, bx + s * 1.25, s * 1.24), s * .15, outline=color, width=max(1, int(s * .07)))
    d.rectangle((bx + s * .14, s * .8, bx + s * 1.0, s * 1.1), fill=color)
    for i in range(4):
        h = s * (.25 + i * .14)
        d.rectangle((bx - s * 1.7 + i * s * .3, s * 1.18 - h, bx - s * 1.5 + i * s * .3, s * 1.18), fill=color)


def nav_bar(d, sw, sh, s):
    y = sh - s * 3.1
    d.rectangle((0, y, sw, sh), fill="white")  # feed scrolls under the bar
    d.line([(0, y), (sw, y)], fill=(225, 225, 228), width=1)
    cy = y + s * 1.15
    for i in range(5):
        cx = sw * (i + .5) / 5
        r = s * .48
        if i == 0:
            d.polygon([(cx - r, cy), (cx, cy - r * 1.05), (cx + r, cy), (cx + r, cy + r), (cx - r, cy + r)], fill=INK)
        elif i == 1:
            d.ellipse((cx - r * .8, cy - r * .8, cx + r * .5, cy + r * .5), outline=INK, width=max(2, int(s * .09)))
            d.line([(cx + r * .4, cy + r * .4), (cx + r, cy + r)], fill=INK, width=max(2, int(s * .1)))
        elif i == 2:
            d.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), r * .3, outline=INK, width=max(2, int(s * .09)))
            d.line([(cx, cy - r * .5), (cx, cy + r * .5)], fill=INK, width=max(2, int(s * .09)))
            d.line([(cx - r * .5, cy), (cx + r * .5, cy)], fill=INK, width=max(2, int(s * .09)))
        elif i == 3:
            d.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), r * .3, outline=INK, width=max(2, int(s * .09)))
            d.polygon([(cx - r * .3, cy - r * .35), (cx + r * .45, cy), (cx - r * .3, cy + r * .35)], fill=INK)
        else:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(205, 205, 210))
    d.rounded_rectangle((sw * .34, sh - s * .75, sw * .66, sh - s * .52), s, fill=INK)


def ig_post_screen(sw, sh, posts, handle, label, caption):
    """Home feed: one or more posts stacked under the Instagram header."""
    s = sw / 22
    im = Image.new("RGB", (sw, sh), "white")
    d = ImageDraw.Draw(im)
    status_bar(d, sw, s)
    d.text((s * 1.1, s * 3.1), "Instagram", font=font(s * 1.45, True), fill=INK, anchor="lm")
    heart(d, sw - s * 4.4, s * 2.55, s * 1.1, w=max(2, int(s * .1)))
    y = s * 4.6
    for k, post in enumerate(posts):
        avatar(im, d, int(s * 2.1), int(y + s * 1.35), int(s * .95), label)
        d.text((s * 3.5, y + s * 1.35), handle, font=font(s * .78, True), fill=INK, anchor="lm")
        d.text((sw - s * 1.2, y + s * 1.2), "•••", font=font(s * .7, True), fill=INK, anchor="rm")
        y += s * 2.7
        ph = round(post.height * sw / post.width)
        im.paste(fit_width(post, sw), (0, int(y)))
        y += ph + s * .7
        icons_row(d, s * 1.0, y, s * 1.1, sw - s * 2.1)
        y += s * 1.9
        d.text((s * 1.0, y), f"{[1248, 986, 2310, 744][k % 4]:,} likes", font=font(s * .74, True), fill=INK)
        y += s * 1.15
        d.text((s * 1.0, y), handle, font=font(s * .74, True), fill=INK)
        tw = d.textlength(handle + " ", font=font(s * .74, True))
        d.text((s * 1.0 + tw, y), caption, font=font(s * .74), fill=INK)
        y += s * 1.15
        d.text((s * 1.0, y), "View all comments", font=font(s * .7), fill=GREY)
        y += s * 1.9
    nav_bar(d, sw, sh, s)
    return im


def ig_profile_screen(sw, sh, tiles, handle, label, name, bio):
    s = sw / 22
    im = Image.new("RGB", (sw, sh), "white")
    d = ImageDraw.Draw(im)
    status_bar(d, sw, s)
    d.text((sw / 2, s * 3.1), handle, font=font(s * .95, True), fill=INK, anchor="mm")
    y = s * 4.4
    avatar(im, d, int(s * 3.4), int(y + s * 2.3), int(s * 2.1), label)
    for i, (n, l) in enumerate((("128", "posts"), ("4,872", "followers"), ("312", "following"))):
        cx = s * (9.3 + i * 4.6)
        d.text((cx, y + s * 1.9), n, font=font(s * .95, True), fill=INK, anchor="mm")
        d.text((cx, y + s * 3.0), l, font=font(s * .7), fill=INK, anchor="mm")
    y += s * 5.1
    d.text((s * 1.2, y), name, font=font(s * .78, True), fill=INK)
    d.text((s * 1.2, y + s * 1.1), bio, font=font(s * .74), fill=INK)
    y += s * 2.7
    bw = (sw - s * 3.4) / 2
    for i, t in enumerate(("Following", "Message")):
        x0 = s * 1.2 + i * (bw + s)
        d.rounded_rectangle((x0, y, x0 + bw, y + s * 1.6), s * .4, fill=(239, 239, 241))
        d.text((x0 + bw / 2, y + s * .8), t, font=font(s * .74, True), fill=INK, anchor="mm")
    y += s * 2.6
    d.line([(0, y + s * 1.9), (sw / 3, y + s * 1.9)], fill=INK, width=max(2, int(s * .08)))
    for i in range(3):
        cx = sw * (i + .5) / 3
        r = s * .45
        if i == 0:
            for gx in range(3):
                for gy in range(3):
                    d.rectangle((cx - r + gx * r * .7, y + s * .5 + gy * r * .7,
                                 cx - r + gx * r * .7 + r * .55, y + s * .5 + gy * r * .7 + r * .55), fill=INK)
        else:
            d.rounded_rectangle((cx - r, y + s * .5, cx + r, y + s * .5 + 2 * r), r * .3, outline=GREY, width=2)
    y += s * 2.1
    gap = max(2, int(s * .1))
    tw = (sw - 2 * gap) / 3
    for i, t in enumerate(tiles):
        x0 = int((i % 3) * (tw + gap))
        y0 = int(y + (i // 3) * (tw * 1.33 + gap))
        im.paste(fit_cover(t, (int(tw), int(tw * 1.33))), (x0, y0))
    nav_bar(d, sw, sh, s)
    return im


def ig_reel_screen(sw, sh, art, handle, label, caption):
    s = sw / 22
    if art.width / art.height > .7:
        # square art: centre it over a blurred fill, as Reels does
        im = fit_cover(art, (sw, sh)).filter(ImageFilter.GaussianBlur(sw / 18))
        fg = fit_width(art, sw)
        im.paste(fg, (0, int(sh * .42 - fg.height / 2)))
    else:
        im = fit_cover(art, (sw, sh))
    shade = Image.linear_gradient("L").resize((sw, sh)).point(lambda v: int(max(0, v - 150) * 1.4))
    im = Image.composite(Image.new("RGB", (sw, sh), (0, 0, 0)), im, shade)
    d = ImageDraw.Draw(im)
    status_bar(d, sw, s, "white")
    d.text((s * 1.2, s * 3.1), "Reels", font=font(s * 1.2, True), fill="white", anchor="lm")
    x = sw - s * 2.4
    for i, n in enumerate(("12.4K", "318", "1,027")):
        y = sh * .52 + i * s * 3.1
        if i == 0:
            heart(d, x - s * .1, y, s * 1.3, fill="white")
        elif i == 1:
            d.ellipse((x, y, x + s * 1.2, y + s * 1.2), outline="white", width=max(2, int(s * .1)))
        else:
            d.polygon([(x - s * .05, y + s * .05), (x + s * 1.25, y + s * .05), (x + s * .5, y + s * 1.2)],
                      outline="white", width=max(2, int(s * .1)))
        d.text((x + s * .55, y + s * 1.85), n, font=font(s * .62, True), fill="white", anchor="mm")
    y = sh - s * 7.2
    avatar(im, d, int(s * 2.0), int(y + s * .9), int(s * .9), label)
    d.text((s * 3.4, y + s * .9), handle, font=font(s * .8, True), fill="white", anchor="lm")
    d.text((s * 1.2, y + s * 2.4), caption, font=font(s * .74), fill="white")
    nav_bar(d, sw, sh, s)
    return im


def phone(base, cx, bottom, h, screen_fn):
    """iPhone-style body with a rendered screen, bottom-centred at (cx, bottom)."""
    w = int(h / 2.06)
    body = Image.new("RGB", (w, h), (28, 28, 30))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle((2, 2, w - 3, h - 3), int(w * .17), outline=(70, 70, 74), width=max(2, w // 120))
    inset = int(w * .035)
    sw, sh = w - 2 * inset, h - 2 * inset
    screen = screen_fn(sw, sh)
    body.paste(screen, (inset, inset), rounded((sw, sh), int(w * .135)))
    bd.rounded_rectangle((w * .37, inset + sh * .014, w * .63, inset + sh * .014 + w * .075), w, fill=(8, 8, 10))
    mask = rounded((w, h), int(w * .17))
    paste_object(base, body, mask, (int(cx - w / 2), int(bottom - h)), blur=22, off=(0, 18), opacity=.38)


# ── devices and print ────────────────────────────────────────────

def laptop(base, cx, bottom, w, art, browser=False):
    sw = int(w * .78)
    sh = int(sw / 1.6)
    bez = int(sw * .035)
    lid = Image.new("RGB", (sw + 2 * bez, sh + 2 * bez), (24, 24, 26))
    screen = Image.new("RGB", (sw, sh), "white")
    y0 = 0
    if browser:
        bar = int(sh * .075)
        d = ImageDraw.Draw(screen)
        d.rectangle((0, 0, sw, bar), fill=(236, 236, 238))
        for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
            d.ellipse((bar * .5 + i * bar * .55, bar * .35, bar * .5 + i * bar * .55 + bar * .3, bar * .65), fill=c)
        d.rounded_rectangle((sw * .3, bar * .22, sw * .7, bar * .78), bar, fill="white")
        y0 = bar
    screen.paste(fit_cover(art, (sw, sh - y0)), (0, y0))
    lid.paste(screen, (bez, bez))
    lmask = rounded(lid.size, int(bez * 1.4))
    lx = int(cx - lid.width / 2)
    ly = int(bottom - lid.height - w * .035)
    paste_object(base, lid, lmask, (lx, ly), blur=24, off=(0, 14), opacity=.3)
    # aluminium base
    bh = int(w * .035)
    deck = Image.new("RGB", (w, bh))
    g = Image.linear_gradient("L").resize((w, bh))
    deck = Image.composite(Image.new("RGB", (w, bh), (150, 150, 155)), Image.new("RGB", (w, bh), (214, 214, 218)), g)
    dm = Image.new("L", (w, bh), 0)
    ImageDraw.Draw(dm).rounded_rectangle((0, 0, w - 1, bh - 1), bh // 2, fill=255)
    ImageDraw.Draw(deck).rounded_rectangle((w * .43, 0, w * .57, bh * .35), bh // 4, fill=(170, 170, 175))
    paste_object(base, deck, dm, (int(cx - w / 2), int(bottom - bh)), blur=14, off=(0, 8), opacity=.35)


def monitor(base, cx, bottom, w, art):
    sw = w
    sh = int(sw * 9 / 16)
    bez = int(sw * .022)
    chin = int(sw * .07)
    body = Image.new("RGB", (sw + 2 * bez, sh + 2 * bez + chin), (226, 226, 230))
    d = ImageDraw.Draw(body)
    d.rectangle((0, 0, body.width, sh + 2 * bez), fill=(22, 22, 24))
    body.paste(fit_cover(art, (sw, sh)), (bez, bez))
    mask = rounded(body.size, int(bez * 1.2))
    neck_h = int(sw * .16)
    top = int(bottom - body.height - neck_h)
    # stand
    neck = Image.new("RGB", (int(sw * .16), neck_h), (198, 198, 203))
    ImageDraw.Draw(neck).rectangle((0, neck_h - int(sw * .012), neck.width, neck_h), fill=(175, 175, 180))
    paste_object(base, neck, Image.new("L", neck.size, 255), (int(cx - neck.width / 2), bottom - neck_h),
                 blur=10, off=(0, 4), opacity=.25)
    paste_object(base, body, mask, (int(cx - body.width / 2), top), blur=26, off=(0, 16), opacity=.3)


def sheet(base, art, cx, cy, h, angle, stack=0):
    art = light(trim(art), .07)
    w = int(h * art.width / art.height)
    pg = art.resize((w, h), Image.LANCZOS)
    for k in range(stack, 0, -1):
        blank = Image.new("RGB", (w, h), (250, 249, 246))
        put_rotated(base, blank, cx + k * 10 * X, cy + k * 6 * X, angle + k * 2.2)
    put_rotated(base, pg, cx, cy, angle)


def put_rotated(base, im, cx, cy, angle, **kw):
    rgba = im.convert("RGBA")
    rgba.putalpha(255)
    rot = rgba.rotate(angle, expand=True, resample=Image.BICUBIC)
    pos = (int(cx - rot.width / 2), int(cy - rot.height / 2))
    paste_object(base, rot.convert("RGB"), rot.getchannel("A"), pos, **kw)


def lightbox(base, cx, bottom, h, art):
    """Backlit city panel in a dark aluminium frame on two posts."""
    art = trim(art)
    fr = int(h * .035)
    ph = int(h * .86)
    pw = int(ph * art.width / art.height)
    panel = art.resize((pw, ph), Image.LANCZOS)
    glow = Image.new("RGB", (pw, ph), (255, 255, 255))
    panel = Image.blend(panel, glow, .04)
    box = Image.new("RGB", (pw + 2 * fr, ph + 2 * fr), (44, 45, 48))
    d = ImageDraw.Draw(box)
    d.rectangle((fr * .45, fr * .45, box.width - fr * .45, box.height - fr * .45), outline=(78, 79, 84), width=max(2, fr // 6))
    box.paste(panel, (fr, fr))
    legs = h - box.height
    for lx in (cx - box.width * .32, cx + box.width * .32):
        post = Image.new("RGB", (int(fr * .9), legs), (52, 53, 56))
        paste_object(base, post, Image.new("L", post.size, 255), (int(lx - post.width / 2), bottom - legs),
                     blur=6, off=(0, 2), opacity=.25)
    paste_object(base, box, Image.new("L", box.size, 255), (int(cx - box.width / 2), bottom - h),
                 blur=30, off=(0, 22), opacity=.32)
    floor = Image.new("L", base.size, 0)
    ImageDraw.Draw(floor).ellipse((cx - box.width * .55, bottom - 10 * X, cx + box.width * .55, bottom + 10 * X), fill=70)
    floor = floor.filter(ImageFilter.GaussianBlur(8 * X))
    base.paste(Image.new("RGB", base.size, (60, 52, 40)), (0, 0), floor)


# ── scenes ───────────────────────────────────────────────────────
# Card sizes (1×): full tray 1230×451 · half tray 608×451 · overview 622×495

def reingold():
    c = scene(608, 451)
    laptop(c, 304 * X, 415 * X, 520 * X, trim(load("reingold-red-talks-ppt")))
    save(c, "mock-reingold-red-talks-ppt")

    c = scene(1230, 451)
    for i, (a, dx) in enumerate(((-5, -330), (1.5, 0), (6, 330))):
        sheet(c, load(f"reingold-dc-health-{i + 1}"), (615 + dx) * X, 232 * X, 370 * X, a, stack=1 if i == 1 else 0)
    save(c, "mock-reingold-dc-health")


def capx():
    posts = [load(f"capx-expo-social-{i}") for i in range(1, 9)]
    posts = [trim(p) for p in posts]
    reels = []
    for i in (1, 2):
        r = load(f"capx-expo-reel-{i}")
        r = r.crop((0, 0, int(r.width * .78), r.height))  # drop the QR code
        reels.append(trim(r))
    handle, label = "saic.capx", "C"
    c = scene(1230, 451)
    H = 420 * X
    xs = [190, 470, 760, 1040]
    phone(c, xs[0] * X, 440 * X, H, lambda w, h: ig_profile_screen(
        w, h, posts + [reels[0]], handle, label, "SAIC Career & Professional Experience", "Prepare & connect."))
    phone(c, xs[1] * X, 440 * X, H, lambda w, h: ig_post_screen(
        w, h, [posts[0]], handle, label, "Expo prep starts now"))
    phone(c, xs[2] * X, 440 * X, H, lambda w, h: ig_reel_screen(w, h, reels[0], handle, label, "5 days to go"))
    phone(c, xs[3] * X, 440 * X, H, lambda w, h: ig_reel_screen(w, h, reels[1], handle, label, "EXPO is today!"))
    save(c, "mock-capx-expo-social")

    c = scene(1230, 451)
    for k, x in enumerate((205, 615, 1025)):
        ig = trim(load(f"capx-ee-social-{k + 1}"))
        eg = trim(load(f"capx-ee-social-{k + 4}"))
        phone(c, x * X, 440 * X, H, lambda w, h, ig=ig, eg=eg: ig_post_screen(
            w, h, [ig, eg], handle, label, "Book a 1:1 with an expert"))
    save(c, "mock-capx-ee-social")


def esri():
    handle, label = "esri", "e"
    c = scene(1230, 451)
    H = 420 * X
    for k, x in enumerate((190, 470, 750)):
        p = trim(load(f"esri-social-{k + 1}"))
        phone(c, x * X, 440 * X, H, lambda w, h, p=p: ig_post_screen(
            w, h, [p], handle, label, "Explore the Expo at #EsriUC"))
    wide = [trim(load(f"esri-social-{k}")) for k in (4, 8)]
    phone(c, 1030 * X, 440 * X, H, lambda w, h: ig_post_screen(
        w, h, wide, handle, label, "See you in San Diego"))
    save(c, "mock-esri-social")

    c = scene(622, 495)
    monitor(c, 311 * X, 455 * X, 470 * X, load("esri-asia-pacific"))
    save(c, "mock-esri-asia-pacific")


def vertical():
    handle, label = "vertical.inc", "V"
    c = scene(1230, 451)
    H = 420 * X
    for k, x in enumerate((150, 380, 615, 850)):
        p = trim(load(f"vertical-instagram-{k + 1}"))
        phone(c, x * X, 440 * X, H, lambda w, h, p=p: ig_post_screen(
            w, h, [p], handle, label, "How we help, in four cards"))
    anim = trim(load("vertical-animation"))
    phone(c, 1080 * X, 440 * X, H, lambda w, h: ig_reel_screen(w, h, anim, handle, label, "40% of city traffic…"))
    save(c, "mock-vertical-social")


def harris():
    c = scene(1230, 451, top=(236, 233, 228), bottom=(214, 209, 200))
    for k, x in enumerate((270, 615, 960)):
        lightbox(c, x * X, 438 * X, 420 * X, load(f"harris-lines-city-panel-{k + 1}"))
    save(c, "mock-harris-lines-city-panels")


if __name__ == "__main__":
    reingold()
    capx()
    esri()
    vertical()
    harris()
