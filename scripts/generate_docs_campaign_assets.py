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

qa = {
    'text_overflow': [],
    'box_overflow': [],
    'card_containment_issues': [],
    'text_box_containment_issues': [],
    'asset': None,
    'text_count': 0,
    'layer_count': 0,
}


def inside(inner, outer, padding=0):
    ix1, iy1, ix2, iy2 = inner
    ox1, oy1, ox2, oy2 = outer
    return ix1 >= ox1 + padding and iy1 >= oy1 + padding and ix2 <= ox2 - padding and iy2 <= oy2 - padding


def check_card_containment(label, kind, bbox, card_box, padding=18):
    if not inside(bbox, card_box, padding):
        qa['card_containment_issues'].append({
            'label': label,
            'kind': kind,
            'bbox': tuple(round(v, 2) for v in bbox),
            'card_box': card_box,
            'padding': padding,
        })


def check_text_box_containment(label, bbox, text_box, padding=0):
    if not inside(bbox, text_box, padding):
        qa['text_box_containment_issues'].append({
            'label': label,
            'bbox': tuple(round(v, 2) for v in bbox),
            'text_box': text_box,
            'padding': padding,
        })


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
    target_w = 330
    logo = logo.resize((target_w, int(logo.height * target_w / logo.width)), Image.Resampling.LANCZOS)
    im.alpha_composite(logo, (W - target_w - 70, 58))


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


def chip(draw, xy, s, fill, f=None, return_box=False):
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
    box = (x, y, x + w, y + h)
    if return_box:
        return w, h, box
    return w, h


def arrow(draw, p1, p2, fill=COL['honey'], width=7):
    draw.line([p1, p2], fill=fill, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    sz = 22
    pts = [
        p2,
        (p2[0] - sz * math.cos(ang - math.pi / 6), p2[1] - sz * math.sin(ang - math.pi / 6)),
        (p2[0] - sz * math.cos(ang + math.pi / 6), p2[1] - sz * math.sin(ang + math.pi / 6)),
    ]
    draw.polygon(pts, fill=fill)


def layer_card(draw, box, title, subtitle, accent, pills):
    qa['layer_count'] += 1
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 12, y1 + 16, x2 + 12, y2 + 16), radius=34, fill=(0, 0, 0, 72))
    draw.rounded_rectangle(box, radius=34, fill=COL['card'], outline=COL['stroke'], width=3)
    draw.rounded_rectangle((x1 + 28, y1 + 34, x1 + 50, y2 - 34), radius=11, fill=accent)
    title_box = draw_text(draw, (x1 + 86, y1 + 32), title, font_semi(42), COL['white'], maxw=620, label=title)
    check_card_containment(title, 'title', title_box, box, padding=34)
    byline_box = (x1 + 76, y1 + 88, min(x1 + 930, x2 - 520), y1 + 140)
    draw.rounded_rectangle(byline_box, radius=18, fill=COL['cream'], outline=accent, width=3)
    subtitle_box = draw_text(draw, (x1 + 100, y1 + 101), subtitle, font_semi(21), COL['ink'], maxw=byline_box[2] - byline_box[0] - 48, spacing=4, label=title + ' subtitle')
    check_card_containment(title + ' subtitle', 'subtitle', subtitle_box, box, padding=34)
    check_text_box_containment(title + ' subtitle', subtitle_box, byline_box, padding=11)
    px, py = x2 - 500, y1 + 72
    for pill in pills:
        w, h, pill_box = chip(draw, (px, py), pill, COL['cream'], font_semi(22), return_box=True)
        check_card_containment(pill, 'pill', pill_box, box, padding=34)
        px += w + 14
        if px > x2 - 78:
            px, py = x2 - 500, py + h + 14


def docs_stack_diagram():
    render_logo()
    im = cover_bg(BG)
    add_logo(im)
    d = ImageDraw.Draw(im)

    draw_text(d, (70, 126), 'The Stoffel stack', font_bold(84), COL['white'], label='title')
    draw_text(
        d,
        (72, 230),
        'Trace the app-facing path from product code to private MPC execution.',
        font_reg(36),
        COL['muted'],
        maxw=1200,
        spacing=9,
        label='subtitle',
    )
    layers = [
        ((130, 330, 1670, 500), 'App integration', 'Rust SDK maps product values into programs.', COL['teal'], ['Rust SDK', 'bindings', 'clients']),
        ((190, 520, 1610, 690), 'Language + CLI', 'Write .stfl, check/build/dev, produce .stflb.', COL['honey'], ['.stfl source', 'CLI', 'Stoffel.toml']),
        ((250, 710, 1550, 880), 'Bytecode + VM', 'The VM separates clear values from shares.', COL['green'], ['.stflb', 'register VM', 'builtins']),
        ((310, 900, 1490, 1070), 'MPC runtime', 'Parties compute over shares; outputs are explicit.', COL['pink'], ['coordinator', 'parties', 'outputs']),
    ]

    for box, title, sub, accent, pills in layers:
        layer_card(d, box, title, sub, accent, pills)

    for (a_box, *_), (b_box, *__) in zip(layers, layers[1:]):
        ax = (a_box[0] + a_box[2]) // 2
        bx = (b_box[0] + b_box[2]) // 2
        arrow(d, (ax, a_box[3] + 12), (bx, b_box[1] - 14), COL['honey'], 7)

    out = OUT / 'stoffel-stack-ecosystem-v6.png'
    im.convert('RGB').save(out, quality=94, optimize=True)
    qa['asset'] = {'path': str(out), 'width': W, 'height': H, 'bytes': out.stat().st_size}
    QA_PATH.write_text(json.dumps(qa, indent=2), encoding='utf-8')
    return out


if __name__ == '__main__':
    path = docs_stack_diagram()
    print(json.dumps({'generated': str(path), **qa}, indent=2))
