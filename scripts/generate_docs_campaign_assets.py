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
    draw.rounded_rectangle((x1 + 24, y1 + 30, x1 + 42, y2 - 30), radius=9, fill=accent)
    title_box = draw_text(draw, (x1 + 72, y1 + 30), title, font_semi(36), COL['white'], maxw=520, label=title)
    check_card_containment(title, 'title', title_box, box, padding=30)
    byline_box = (x1 + 62, y1 + 78, min(x1 + 850, x2 - 590), y1 + 124)
    draw.rounded_rectangle(byline_box, radius=16, fill=COL['cream'], outline=accent, width=2)
    subtitle_box = draw_text(draw, (x1 + 82, y1 + 89), subtitle, font_semi(19), COL['ink'], maxw=byline_box[2] - byline_box[0] - 40, spacing=4, label=title + ' subtitle')
    check_card_containment(title + ' subtitle', 'subtitle', subtitle_box, box, padding=30)
    check_text_box_containment(title + ' subtitle', subtitle_box, byline_box, padding=10)
    px, py = x2 - 512, y1 + 62
    for pill in pills:
        w, h, pill_box = chip(draw, (px, py), pill, (255, 248, 224, 238), font_semi(19), return_box=True)
        check_card_containment(pill, 'pill', pill_box, box, padding=30)
        px += w + 12
        if px > x2 - 70:
            px, py = x2 - 512, py + h + 12


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
    layers = [
        ((165, 352, 1635, 502), 'App integration', 'Rust SDK maps product values into programs.', COL['teal'], ['Rust SDK', 'bindings', 'clients']),
        ((215, 528, 1585, 678), 'Language + CLI', 'Write .stfl, check/build/dev, produce .stflb.', COL['honey'], ['.stfl source', 'CLI', 'Stoffel.toml']),
        ((265, 704, 1535, 854), 'Bytecode + VM', 'The VM separates clear values from shares.', COL['green'], ['.stflb', 'register VM', 'builtins']),
        ((315, 880, 1485, 1030), 'MPC runtime', 'Parties compute over shares; outputs are explicit.', COL['pink'], ['coordinator', 'parties', 'outputs']),
    ]

    for box, title, sub, accent, pills in layers:
        layer_card(d, box, title, sub, accent, pills)

    for (a_box, *_), (b_box, *__) in zip(layers, layers[1:]):
        ax = (a_box[0] + a_box[2]) // 2
        bx = (b_box[0] + b_box[2]) // 2
        arrow(d, (ax, a_box[3] + 10), (bx, b_box[1] - 12), COL['honey'], 5)

    # Subtle source note, not a competing visual element.
    draw_text(d, (70, 1080), 'Source: Stoffel docs + 0.1.0 component model', font_reg(20), COL['muted'], label='source note')

    out = OUT / 'stoffel-stack-ecosystem-v3.png'
    im.convert('RGB').save(out, quality=94, optimize=True)
    qa['asset'] = {'path': str(out), 'width': W, 'height': H, 'bytes': out.stat().st_size}
    QA_PATH.write_text(json.dumps(qa, indent=2), encoding='utf-8')
    return out


if __name__ == '__main__':
    path = docs_stack_diagram()
    print(json.dumps({'generated': str(path), **qa}, indent=2))
