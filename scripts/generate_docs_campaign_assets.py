from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import math
import re
import cairosvg

ROOT = Path('/workspace/internal-skills/design')
OUT = Path('images/campaign')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1800, 1125
BG = ROOT / 'Backgrounds/Main-hero-bg.png'
LOGO_SVG = ROOT / 'brand_assets/Logo/SVG/Full-logo-mark-SVG.svg'
LOGO_RENDERED = OUT / 'derived-full-logo-mark-white-transparent.png'
FONTS = ROOT / 'brand_assets/Ambit Full Family'
QA_PATH = OUT / 'docs-campaign-qa.json'

font_reg = lambda s: ImageFont.truetype(str(FONTS / 'ambit-regular.otf'), s)
font_semi = lambda s: ImageFont.truetype(str(FONTS / 'ambit-semibold.otf'), s)
font_bold = lambda s: ImageFont.truetype(str(FONTS / 'ambit-bold.otf'), s)

COL = {
    'cream': (255, 248, 224, 255),
    'white': (255, 255, 255, 255),
    'muted': (218, 227, 235, 240),
    'soft': (236, 242, 248, 245),
    'honey': (253, 196, 72, 255),
    'teal': (82, 202, 194, 255),
    'green': (129, 215, 176, 255),
    'pink': (255, 169, 156, 255),
    'ink': (7, 17, 32, 255),
    'navy': (5, 12, 28, 235),
    'card': (9, 26, 54, 224),
    'stroke': (255, 255, 255, 84),
}

qa = {'text_overflow': [], 'box_overflow': [], 'asset': None, 'text_count': 0, 'layer_count': 0}


def render_logo():
    svg = LOGO_SVG.read_text()
    svg = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="white"', svg)
    svg = re.sub(r'fill:#[0-9A-Fa-f]{6}', 'fill:white', svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(LOGO_RENDERED), output_width=720)


def cover_bg(path):
    im = Image.open(path).convert('RGBA')
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im.alpha_composite(Image.new('RGBA', (W, H), (0, 8, 24, 116)))
    return im


def add_logo(im):
    logo = Image.open(LOGO_RENDERED).convert('RGBA')
    target_w = 248
    logo = logo.resize((target_w, int(logo.height * target_w / logo.width)), Image.Resampling.LANCZOS)
    im.alpha_composite(logo, (70, 58))


def wrap(draw, s, font, maxw):
    lines = []
    words = s.split()
    line = ''
    for word in words:
        test = (line + ' ' + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= maxw or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(draw, xy, s, font, fill, maxw=None, spacing=6, label='text'):
    if maxw:
        content = '\n'.join(wrap(draw, s, font, maxw))
        draw.multiline_text(xy, content, font=font, fill=fill, spacing=spacing)
        bbox = draw.multiline_textbbox(xy, content, font=font, spacing=spacing)
    else:
        draw.text(xy, s, font=font, fill=fill)
        bbox = draw.textbbox(xy, s, font=font)
    qa['text_count'] += 1
    if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > W or bbox[3] > H:
        qa['text_overflow'].append({'label': label, 'bbox': bbox})
    return bbox


def chip(draw, xy, s, fill, f=None):
    f = f or font_semi(20)
    bbox = draw.textbbox((0, 0), s, font=f)
    x, y = xy
    pad_x, pad_y = 16, 9
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill)
    draw.text((x + pad_x, y + pad_y - 2), s, font=f, fill=COL['ink'])
    if x + w > W or y + h > H:
        qa['box_overflow'].append({'label': s, 'box': (x, y, x + w, y + h)})
    return w, h


def arrow(draw, p1, p2, fill=COL['honey'], width=5):
    draw.line([p1, p2], fill=fill, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    sz = 18
    pts = [
        p2,
        (p2[0] - sz * math.cos(ang - math.pi / 6), p2[1] - sz * math.sin(ang - math.pi / 6)),
        (p2[0] - sz * math.cos(ang + math.pi / 6), p2[1] - sz * math.sin(ang + math.pi / 6)),
    ]
    draw.polygon(pts, fill=fill)


def layer_card(draw, box, title, subtitle, accent, pills):
    qa['layer_count'] += 1
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 10, y1 + 14, x2 + 10, y2 + 14), radius=28, fill=(0, 0, 0, 68))
    draw.rounded_rectangle(box, radius=28, fill=COL['card'], outline=COL['stroke'], width=2)
    draw.rounded_rectangle((x1 + 22, y1 + 24, x1 + 38, y2 - 24), radius=8, fill=accent)
    draw_text(draw, (x1 + 62, y1 + 24), title, font_semi(34), COL['white'], maxw=520, label=title)
    draw_text(draw, (x1 + 62, y1 + 74), subtitle, font_reg(24), COL['muted'], maxw=620, spacing=5, label=title + ' subtitle')
    px, py = x2 - 560, y1 + 42
    for pill in pills:
        w, h = chip(draw, (px, py), pill, (255, 248, 224, 238), font_semi(19))
        px += w + 12
        if px > x2 - 78:
            px, py = x2 - 560, py + h + 12


def docs_stack_diagram():
    render_logo()
    im = cover_bg(BG)
    add_logo(im)
    d = ImageDraw.Draw(im)

    draw_text(d, (70, 156), 'The Stoffel stack', font_bold(72), COL['white'], label='title')
    draw_text(
        d,
        (72, 246),
        'A docs-first view of how app code moves through the Stoffel toolchain into VM-backed MPC execution.',
        font_reg(31),
        COL['muted'],
        maxw=1180,
        spacing=8,
        label='subtitle',
    )
    chip(d, (72, 328), 'Docs overview', COL['honey'])
    chip(d, (268, 328), 'CLI + Rust SDK path', COL['teal'])

    layers = [
        ((185, 446, 1615, 560), 'App integration', 'Rust SDK and generated bindings connect product values to Stoffel programs.', COL['teal'], ['Rust SDK', 'typed bindings', 'clients']),
        ((235, 604, 1565, 718), 'Language + CLI', 'Write .stfl, run check/build/dev, and produce a portable .stflb artifact.', COL['honey'], ['.stfl source', 'stoffel CLI', 'Stoffel.toml']),
        ((285, 762, 1515, 876), 'Bytecode + VM', 'The VM loads .stflb functions and separates clear values from secret shares.', COL['green'], ['.stflb', 'register VM', 'builtins']),
        ((335, 920, 1465, 1034), 'MPC runtime', 'Coordinator, networking, and protocols execute over shares and return authorized outputs.', COL['pink'], ['coordinator', 'parties', 'outputs']),
    ]

    for box, title, sub, accent, pills in layers:
        layer_card(d, box, title, sub, accent, pills)

    for (a_box, *_), (b_box, *__) in zip(layers, layers[1:]):
        ax = (a_box[0] + a_box[2]) // 2
        bx = (b_box[0] + b_box[2]) // 2
        arrow(d, (ax, a_box[3] + 10), (bx, b_box[1] - 12), COL['honey'], 5)

    # Subtle source note, not a competing visual element.
    draw_text(d, (70, 1068), 'Source: Stoffel docs + 0.1.0 component model', font_reg(20), COL['muted'], label='source note')

    out = OUT / 'stoffel-stack-docs.png'
    im.convert('RGB').save(out, quality=94, optimize=True)
    qa['asset'] = {'path': str(out), 'width': W, 'height': H, 'bytes': out.stat().st_size}
    QA_PATH.write_text(json.dumps(qa, indent=2), encoding='utf-8')
    return out


if __name__ == '__main__':
    path = docs_stack_diagram()
    print(json.dumps({'generated': str(path), **qa}, indent=2))
