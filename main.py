SEED = 20261119
WEEKDAY = 'THURSDAY'
BIG_DATE = '19 NOVEMBER 2026'
DATE_LINE = '19.11.2026'
HERO_KICKER = 'SHENZHEN · APEC'
HERO = 'TRUMP, XI, PUTIN: THE TRILATERAL MEETS'
DEK = 'The three nuclear powers at one table in Shenzhen — over Ukraine, Iran and a fragile trade truce.'
FOOTER = 'MAKE.FUN NEWS IMAGE · 19 NOV 2026 · SOURCES: REUTERS, USNEWS, XINHUA, TIMES OF INDIA, AA'
STORIES = [
    ('SHENZHEN · APEC', 'Trilateral convenes; Xi hails open trade, Putin defies sanctions', 'Reuters · Xinhua'),
    ('EUROPE · UKRAINE', 'EU €45bn Ukraine loan on the table; Kyiv braces for winter', 'Reuters · The Guardian'),
    ('IRAN WAR', 'US hit Qeshm; drones fired at Ali Al Salem as Bahrain intercepts', 'Just Security · Xinhua'),
    ('INDIA', 'Cyclone Akvan to strike Andhra Pradesh coast on Nov 20', 'The Times of India'),
    ('UNITED STATES', 'NSA network down; Apple and Google outages rattle the week', 'Democracy Now · AA'),
    ('SPORT', 'India beat Pakistan 2-1 to lift the SAFF Championship in Dhaka', 'Times of India'),
]
#!/usr/bin/env python3
"""news-image-<day>: one image that sums up the day's world news.

Python 3 standard library only. No network. Deterministic: two runs write
the same bytes. Reads the baked headlines below (compiled from public wire
reports on the day) and renders a 1024x1024 PNG to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os, sys, zlib, struct, random
_here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_here, '_font.py')) as _fh:
    _ns = {}
    exec(_fh.read(), _ns)
    FONT = _ns['FONT']

W = H = 1024
OUT = os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'), 'entry.png')

NAVY_TOP = (11, 16, 38)
NAVY_MID = (24, 32, 64)
GROUND = (7, 9, 18)
GOLD = (232, 184, 109)
WHITE = (245, 246, 250)
GREY = (190, 197, 220)
DIM = (142, 148, 172)

buf = bytearray(W * H * 3)

def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]; buf[i + 1] = c[1]; buf[i + 2] = c[2]

def blend(x, y, c, a):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = int(buf[i] * (1 - a) + c[0] * a)
        buf[i + 1] = int(buf[i + 1] * (1 - a) + c[1] * a)
        buf[i + 2] = int(buf[i + 2] * (1 - a) + c[2] * a)

def rect(x0, y0, x1, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        row = y * W * 3
        for x in range(max(0, x0), min(W, x1)):
            i = row + x * 3
            buf[i] = c[0]; buf[i + 1] = c[1]; buf[i + 2] = c[2]

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# vertical gradient sky: top navy -> mid -> horizon glow -> ground
for y in range(H):
    if y < 620:
        t = y / 620.0
        c = lerp(NAVY_TOP, NAVY_MID, t)
    elif y < 700:
        t = (y - 620) / 80.0
        c = lerp(NAVY_MID, (58, 42, 34), t)   # dusk glow at horizon
    else:
        t = (y - 700) / (H - 700)
        c = lerp((16, 14, 22), GROUND, t)
    rect(0, y, W, y + 1, c)

# stars (deterministic)
rng = random.Random(SEED)
for _ in range(480):
    x = rng.randrange(W); y = rng.randrange(0, 560); r = rng.random()
    a = 0.25 + 0.75 * r
    size = 1 if r < 0.8 else 2
    for dy in range(size):
        for dx in range(size):
            blend(x + dx, y + dy, WHITE, a)

# moon with glow upper-right
MX, MY, MR = 906, 108, 46
for r in range(MR + 60, MR, -1):
    a = max(0.0, 0.28 * (1 - (r - MR) / 60.0))
    for y in range(MY - r, MY + r + 1):
        dx2 = r * r - (y - MY) ** 2
        if dx2 < 0: continue
        dx = int(dx2 ** 0.5)
        for x in range(MX - dx, MX + dx + 1):
            blend(x % W, y, (240, 230, 200), a * 0.35)
for y in range(MY - MR, MY + MR + 1):
    dx2 = MR * MR - (y - MY) ** 2
    if dx2 < 0: continue
    dx = int(dx2 ** 0.5)
    for x in range(MX - dx, MX + dx + 1):
        d = ((x - MX) ** 2 + (y - MY) ** 2) / (MR * MR)
        c = lerp((248, 240, 214), (204, 196, 172), d)
        set_px(x, y, c)
# moon craters
for cx, cy, cr in ((836, 108, 8), (872, 132, 6), (852, 96, 4)):
    for y in range(cy - cr, cy + cr + 1):
        dx2 = cr * cr - (y - cy) ** 2
        if dx2 < 0: continue
        dx = int(dx2 ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            blend(x, y, (150, 144, 124), 0.6)

def draw_char(x, y, ch, scale, color):
    glyph = FONT.get(ch.upper() if ch.upper() in FONT else ' ')
    for gy, row in enumerate(glyph):
        for gx, cell in enumerate(row):
            if cell == '#':
                rect(x + gx * scale, y + gy * scale, x + (gx + 1) * scale, y + (gy + 1) * scale, color)

def text_w(s, scale):
    return len(s) * 6 * scale - scale

def draw_text(x, y, s, scale, color):
    cx = x
    for ch in s:
        draw_char(cx, y, ch, scale, color)
        cx += 6 * scale

def draw_text_centered(y, s, scale, color):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, color)

def wrap(s, scale, max_w):
    words = s.split()
    lines, cur = [], ''
    for w_ in words:
        trial = (cur + ' ' + w_).strip()
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def panel(x0, y0, x1, y1, fill, edge):
    rect(x0, y0, x1, y1, fill)
    rect(x0, y0, x1, y0 + 2, edge)

# --- masthead
rect(0, 0, W, 6, GOLD)
draw_text(28, 22, 'THE WORLD IN ONE IMAGE', 2, GOLD)
draw_text(W - text_w(DATE_LINE, 2) - 28, 22, DATE_LINE, 2, GREY)
draw_text_centered(52, WEEKDAY + ' — ' + BIG_DATE, 2, DIM)
rect(60, 96, 700, 98, DIM)

# --- hero block
draw_text(60, 118, HERO_KICKER, 2, GOLD)
hy = 152
for line in wrap(HERO, 6, 640):
    draw_text(60, hy, line, 6, WHITE)
    hy += 7 * 6 + 6
hy += 8
for line in wrap(DEK, 2, W - 120):
    draw_text(60, hy, line, 2, GREY)
    hy += 7 * 2 + 4

# skyline silhouette above the horizon (deterministic)
sky_rng = random.Random(SEED ^ 0x5EED)
bx = 0
while bx < W:
    bw = sky_rng.randrange(24, 78)
    bh = sky_rng.randrange(40, 175)
    rect(bx, 648 - bh, min(W, bx + bw), 648, (5, 6, 13))
    for wy in range(648 - bh + 6, 644, 12):
        for wx in range(bx + 5, min(W, bx + bw) - 5, 10):
            if sky_rng.random() < 0.16:
                set_px(wx, wy, GOLD)
    bx += bw + sky_rng.randrange(4, 18)

# thin divider with APEC glint
rect(60, 648, W - 60, 650, (70, 60, 44))

# --- tiles (2 cols x 3 rows) below horizon glow
col_w = (W - 60 - 24) // 2
tile_h = 96
start_y = 672
for idx, (kicker, headline, source) in enumerate(STORIES):
    col = idx % 2; row = idx // 2
    x0 = 30 + col * (col_w + 24)
    y0 = start_y + row * (tile_h + 10)
    fill = (17, 21, 40) if row % 2 == 0 else (19, 23, 46)
    panel(x0, y0, x0 + col_w, y0 + tile_h, fill, GOLD)
    draw_text(x0 + 14, y0 + 10, kicker, 1, GOLD)
    ty = y0 + 26
    for line in wrap(headline, 2, col_w - 28):
        draw_text(x0 + 14, ty, line, 2, WHITE)
        ty += 7 * 2 + 3
    draw_text(x0 + 14, y0 + tile_h - 12, source, 1, DIM)

# --- footer
rect(0, H - 26, W, H, (5, 6, 12))
draw_text_centered(H - 18, FOOTER, 1, GREY)

# --- PNG encode
raw = b''.join(b'\x00' + bytes(buf[y * W * 3:(y + 1) * W * 3]) for y in range(H))
comp = zlib.compress(raw, 9)

def chunk(tag, data):
    c = struct.pack('>I', len(data)) + tag + data
    return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', comp)
       + chunk(b'IEND', b''))
try:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
except OSError:
    pass
with open(OUT, 'wb') as f:
    f.write(png)
print('wrote', OUT, len(png), 'bytes')
