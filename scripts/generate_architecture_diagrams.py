#!/usr/bin/env python3
"""Generate lightweight Stoffel architecture diagrams for the docs."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

OUT_DIR = Path(__file__).resolve().parents[1] / "images" / "diagrams"
QA_PATH = OUT_DIR / "diagram-qa.json"
W, H = 1200, 675

CSS = """
:root { color-scheme: light; }
.bg { fill: #f8f8fc; }
.header { fill: #3448f0; }
.title { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 34px; font-weight: 700; fill: #ffffff; }
.subtitle { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 17px; font-weight: 500; fill: #ffffff; }
.zone { fill: #ffffff; stroke: #b8bde8; stroke-width: 2; stroke-dasharray: 9 8; rx: 22; }
.zone-title { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 17px; font-weight: 700; fill: #17214f; letter-spacing: .02em; }
.card { fill: #ffffff; stroke: #c6cbef; stroke-width: 2; rx: 16; }
.card-lav { fill: #ebe9ff; stroke: #c6c0ff; }
.card-cream { fill: #fff6df; stroke: #edd797; }
.card-blue { fill: #3448f0; stroke: #2335c8; }
.card-party { fill: #ffffff; stroke: #3448f0; stroke-width: 3; }
.card-cyan { fill: #e5fbff; stroke: #7be4f5; }
.card-text { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 18px; font-weight: 700; fill: #121a44; }
.card-sub { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 14px; font-weight: 400; fill: #465078; }
.white { fill: #ffffff; }
.on-blue-title { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 18px; font-weight: 700; }
.on-blue-sub { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 14px; font-weight: 700; }
.small { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 13px; font-weight: 400; fill: #465078; }
.badge { fill: #5ee3ff; stroke: #28bfdc; stroke-width: 1.5; }
.badge-text { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 15px; font-weight: 700; fill: #07133d; text-anchor: middle; dominant-baseline: middle; }
.arrow { stroke: #101a45; stroke-width: 3; fill: none; marker-end: url(#arrow); stroke-linecap: round; stroke-linejoin: round; }
.arrow-soft { stroke: #3448f0; stroke-width: 2.5; fill: none; marker-end: url(#arrow-soft); stroke-linecap: round; stroke-linejoin: round; opacity: .85; }
.arrow-dash { stroke: #3448f0; stroke-width: 2.5; fill: none; stroke-dasharray: 7 7; marker-end: url(#arrow-soft); opacity: .72; }
.boundary { stroke: #3448f0; stroke-width: 2.5; fill: none; stroke-dasharray: 8 8; stroke-linecap: round; opacity: .72; }
.label-chip { fill: #ffffff; stroke: #d7daf4; stroke-width: 1; rx: 10; }
.label { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 13px; font-weight: 700; fill: #24305f; text-anchor: middle; dominant-baseline: middle; }
"""

@dataclass
class Diagram:
    name: str
    title: str
    subtitle: str
    body: str


PALETTE = {
    "header": "#3448f0",
    "card-lav": "#ebe9ff",
    "card-cream": "#fff6df",
    "card-blue": "#3448f0",
    "card-party": "#ffffff",
    "card-cyan": "#e5fbff",
    "zone": "#ffffff",
    "label-chip": "#ffffff",
    "badge": "#5ee3ff",
}

TEXT_COLORS = {
    "title": "#ffffff",
    "subtitle": "#ffffff",
    "zone-title": "#17214f",
    "card-text": "#121a44",
    "card-sub": "#465078",
    "white": "#ffffff",
    "on-blue-title": "#ffffff",
    "on-blue-sub": "#ffffff",
    "badge-text": "#07133d",
    "label": "#24305f",
}


def text(x: int, y: int, lines: str | Iterable[str], cls: str = "card-text", anchor: str = "middle", gap: int = 22) -> str:
    if isinstance(lines, str):
        lines = [lines]
    out = []
    for i, line in enumerate(lines):
        attrs = f'class="{cls}"'
        if cls in {"on-blue-title", "on-blue-sub"}:
            # Inline paint attributes make the blue-node text independent of
            # downstream CSS cascade/rendering quirks in docs platforms.
            attrs = f'class="{cls}" fill="#ffffff" opacity="1" style="fill:#ffffff;color:#ffffff"'
        out.append(f'<text x="{x}" y="{y + i * gap}" {attrs} text-anchor="{anchor}">{esc(line)}</text>')
    return "\n".join(out)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    sub: str = "",
    cls: str = "card",
    title_cls: str = "card-text",
    sub_cls: str | None = None,
) -> str:
    body = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}"/>']
    if "card-blue" in cls and title_cls == "card-text":
        title_cls = "on-blue-title"
    body.append(text(x + w // 2, y + 34, title, title_cls))
    if sub:
        if sub_cls is None:
            sub_cls = "on-blue-sub" if "card-blue" in cls else "card-sub"
        body.append(text(x + w // 2, y + 60, sub.split("|"), sub_cls, gap=18))
    return "\n".join(body)


def zone(x: int, y: int, w: int, h: int, title: str) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="zone"/>\n<text x="{x+24}" y="{y+34}" class="zone-title">{esc(title)}</text>'


def arrow(x1: int, y1: int, x2: int, y2: int, cls: str = "arrow") -> str:
    return f'<path d="M{x1},{y1} L{x2},{y2}" class="{cls}"/>'


def curve(d: str, cls: str = "arrow") -> str:
    return f'<path d="{d}" class="{cls}"/>'


def chip(x: int, y: int, w: int, label: str) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="28" class="label-chip"/>\n<text x="{x+w/2:.1f}" y="{y+14}" class="label">{esc(label)}</text>'


def relative_luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    channels = [int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def linearize(channel: float) -> float:
        return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

    r, g, b = [linearize(channel) for channel in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    fg = relative_luminance(foreground)
    bg = relative_luminance(background)
    light, dark = max(fg, bg), min(fg, bg)
    return (light + 0.05) / (dark + 0.05)


def contrast_qa() -> dict:
    pairs = [
        ("header title", "title", "header"),
        ("header subtitle", "subtitle", "header"),
        ("zone label", "zone-title", "zone"),
        ("lavender card title", "card-text", "card-lav"),
        ("lavender card subtitle", "card-sub", "card-lav"),
        ("cream card title", "card-text", "card-cream"),
        ("cream card subtitle", "card-sub", "card-cream"),
        ("party card title", "card-text", "card-party"),
        ("party card subtitle", "card-sub", "card-party"),
        ("cyan card title", "card-text", "card-cyan"),
        ("cyan card subtitle", "card-sub", "card-cyan"),
        ("blue card title", "on-blue-title", "card-blue"),
        ("blue card subtitle", "on-blue-sub", "card-blue"),
        ("badge text", "badge-text", "badge"),
        ("arrow label chip", "label", "label-chip"),
    ]
    checked = []
    issues = []
    for name, text_key, bg_key in pairs:
        ratio = contrast_ratio(TEXT_COLORS[text_key], PALETTE[bg_key])
        item = {
            "pair": name,
            "foreground": TEXT_COLORS[text_key],
            "background": PALETTE[bg_key],
            "contrast_ratio": round(ratio, 2),
        }
        checked.append(item)
        if ratio < 4.5:
            issues.append(item)
    return {"checked": checked, "issues": issues}


def boxes_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float], gap: float = 0) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return ax1 < bx2 + gap and ax2 + gap > bx1 and ay1 < by2 + gap and ay2 + gap > by1


def layout_qa_for_svg(root: ET.Element, diagram_name: str) -> dict:
    rects = []
    texts = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "rect":
            width = float(el.attrib.get("width", 0) or 0)
            height = float(el.attrib.get("height", 0) or 0)
            if not width or not height:
                continue
            x = float(el.attrib.get("x", 0) or 0)
            y = float(el.attrib.get("y", 0) or 0)
            cls = el.attrib.get("class", "")
            rects.append({"class": cls, "box": (x, y, x + width, y + height)})
        elif tag == "text":
            content = "".join(el.itertext()).strip()
            if not content:
                continue
            texts.append({
                "text": content,
                "class": el.attrib.get("class", ""),
                "x": float(el.attrib.get("x", 0) or 0),
                "y": float(el.attrib.get("y", 0) or 0),
            })

    cards = [r for r in rects if "card" in r["class"] and "label-chip" not in r["class"]]
    zones = [r for r in rects if "zone" in r["class"]]
    issues = []
    for item in rects:
        x1, y1, x2, y2 = item["box"]
        if x1 < 0 or y1 < 0 or x2 > W or y2 > H:
            issues.append({"type": "rect_canvas_overflow", "diagram": diagram_name, "class": item["class"], "box": item["box"]})
    for item in texts:
        if item["x"] < 0 or item["x"] > W or item["y"] < 0 or item["y"] > H:
            issues.append({"type": "text_anchor_canvas_overflow", "diagram": diagram_name, **item})
    for i, a in enumerate(cards):
        for b in cards[i + 1:]:
            if boxes_overlap(a["box"], b["box"], gap=0):
                issues.append({"type": "card_overlap", "diagram": diagram_name, "a": a, "b": b})
    if zones:
        for card_item in cards:
            cx1, cy1, cx2, cy2 = card_item["box"]
            if not any(z["box"][0] <= cx1 and z["box"][1] <= cy1 and z["box"][2] >= cx2 and z["box"][3] >= cy2 for z in zones):
                issues.append({"type": "card_outside_zone", "diagram": diagram_name, "card": card_item})
    return {"diagram": diagram_name, "card_count": len(cards), "zone_count": len(zones), "text_count": len(texts), "issues": issues}


def base(diagram: Diagram) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(diagram.title)}</title>
  <desc id="desc">{esc(diagram.subtitle)}</desc>
  <defs>
    <style>{CSS}</style>
    <marker id="arrow" markerWidth="11" markerHeight="11" refX="10" refY="5.5" orient="auto"><path d="M0,0 L11,5.5 L0,11 z" fill="#101a45"/></marker>
    <marker id="arrow-soft" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3448f0"/></marker>
  </defs>
  <rect class="bg" width="{W}" height="{H}"/>
  <rect class="header" x="0" y="0" width="{W}" height="94"/>
  <text x="48" y="40" class="title">{esc(diagram.title)}</text>
  <text x="48" y="68" class="subtitle" fill="#ffffff" opacity="1" style="fill:#ffffff;color:#ffffff">{esc(diagram.subtitle)}</text>
  {diagram.body}
</svg>
'''


def stack() -> Diagram:
    body = "\n".join([
        zone(44, 126, 325, 394, "Developer + application"),
        zone(437, 126, 326, 394, "Build contract"),
        zone(831, 126, 325, 394, "Networked MPC runtime"),
        card(78, 190, 255, 84, ".stfl source", "computation + secret inputs", "card card-lav"),
        card(78, 310, 255, 84, "Rust app / CLI", "maps product values|starts local or network run", "card card-lav"),
        card(470, 184, 260, 90, "compiler", "parse + type check|lower to VM functions", "card card-cream"),
        card(470, 326, 260, 90, ".stflb + manifest", "portable bytecode|input/output contract", "card card-cream"),
        card(864, 180, 258, 82, "coordinator", "lifecycle + IO routing", "card card-cyan"),
        card(852, 318, 118, 82, "party 1", "VM over shares", "card card-blue"),
        card(988, 318, 118, 82, "party 2", "VM over shares", "card card-blue"),
        card(920, 432, 118, 82, "party n", "VM over shares", "card card-blue"),
        arrow(333, 232, 470, 232), chip(357, 200, 95, "build"),
        arrow(333, 352, 470, 370), chip(358, 342, 87, "load/run"),
        arrow(600, 274, 600, 326), chip(538, 288, 124, "emit artifact"),
        arrow(730, 370, 864, 220), chip(751, 278, 100, "same file"),
        curve("M864,242 C780,560 300,560 205,394", "arrow-soft"), chip(434, 536, 292, "authorized output shares/results return"),
        curve("M970,318 C945,280 990,280 1000,318", "arrow-dash"),
        curve("M970,400 C960,428 965,438 920,462", "arrow-dash"),
        curve("M1038,432 C1088,418 1112,386 1106,360", "arrow-dash"),
        chip(1042, 276, 104, "peer rounds"),
    ])
    return Diagram("stoffel-stack", "Stoffel system flow", "Source, build artifact, runtime parties, and authorized outputs", body)


def mpc_flow() -> Diagram:
    body = "\n".join([
        zone(62, 128, 292, 382, "Input owners"),
        zone(454, 128, 292, 382, "MPC parties"),
        zone(846, 128, 292, 382, "Authorized output"),
        card(98, 190, 220, 78, "Alice input", "raw value stays private", "card card-lav"),
        card(98, 332, 220, 78, "Bob input", "raw value stays private", "card card-lav"),
        card(486, 178, 228, 70, "share 1", "one masked fragment", "card card-blue"),
        card(486, 286, 228, 70, "share 2", "one masked fragment", "card card-blue"),
        card(486, 394, 228, 70, "share n", "one masked fragment", "card card-blue"),
        card(886, 228, 212, 86, "opened result", "only the value the|program reveals", "card card-cream"),
        card(886, 366, 212, 74, "private trace", "inputs + intermediates|remain secret", "card card-cyan"),
        '<path d="M404,178 L404,460" class="boundary"/>',
        chip(334, 146, 140, "share split"),
        curve("M318,229 C376,205 420,197 486,213"),
        curve("M318,229 C390,250 420,292 486,321", "arrow-soft"),
        curve("M318,229 C382,316 418,396 486,429", "arrow-soft"),
        curve("M318,371 C380,274 418,224 486,213", "arrow-soft"),
        curve("M318,371 C390,356 424,337 486,321"),
        curve("M318,371 C378,398 422,420 486,429", "arrow-soft"),
        curve("M714,213 C785,220 810,238 886,270"),
        curve("M714,321 C795,320 815,306 886,286"),
        curve("M714,429 C800,420 825,386 886,403", "arrow-soft"),
        chip(750, 174, 120, "compute"),
        chip(770, 462, 150, "not reconstructed"),
    ])
    return Diagram("mpc-privacy-flow", "MPC privacy flow", "Inputs are shared, computed over, and revealed only at explicit output boundaries", body)


def dev_loop() -> Diagram:
    steps = [
        (70, 214, "1", "write", "src/main.stfl"),
        (286, 214, "2", "check", "validate source"),
        (502, 214, "3", "build", ".stflb artifact"),
        (718, 214, "4", "run", "local MPC nodes"),
        (934, 214, "5", "integrate", "Rust SDK wrapper"),
    ]
    parts=[]
    for x,y,n,t,s in steps:
        parts.append(f'<circle cx="{x+35}" cy="{y-32}" r="18" class="badge"/><text x="{x+35}" y="{y-32}" class="badge-text">{n}</text>')
        parts.append(card(x,y,170,92,t,s,"card card-lav" if n in {"1","5"} else "card card-cream"))
    for i in range(len(steps)-1): parts.append(arrow(steps[i][0]+170,260,steps[i+1][0],260))
    parts += [
        curve("M1019,306 C960,496 220,496 155,306", "arrow-soft"),
        chip(444, 484, 312, "edit, rebuild, rerun until the boundary is right"),
        card(318, 398, 564, 68, "Local MPC testing spawns several parties on your machine", "uses parties + threshold settings from Stoffel.toml or CLI flags", "card card-cyan"),
    ]
    return Diagram("developer-loop", "Stoffel development loop", "Check, build, inspect, and run local MPC before application integration", "\n".join(parts))


def compilation() -> Diagram:
    labels=[(".stfl source","program + types"),("parse","AST"),("type check","clear/secret shapes"),("lower","VM functions"),("optimize","instruction stream"),(".stflb","bytecode + manifest")]
    parts=[]
    x=70
    for i,(t,s) in enumerate(labels):
        cls="card card-lav" if i==0 else "card card-cream" if i<5 else "card card-cyan"
        parts.append(card(x,230,150,88,t,s,cls))
        if i<5: parts.append(arrow(x+150,274,x+188,274))
        x+=188
    parts += [card(178,410,270,72,"stoffel check","validate without writing bytecode","card card-lav"),card(482,410,270,72,"stoffel build","write target/debug/*.stflb","card card-lav"),card(786,410,270,72,"disassemble/run","inspect or execute artifact","card card-lav")]
    return Diagram("compilation-pipeline", "Compilation pipeline", "How StoffelLang becomes portable Stoffel VM bytecode", "\n".join(parts))


def sdk_paths() -> Diagram:
    body="\n".join([
        zone(44, 132, 294, 392, "Rust app"),
        zone(392, 132, 326, 392, "Compile or load"),
        zone(774, 132, 382, 392, "Runtime path"),
        card(78,220,226,90,"Rust application","domain types + service logic","card card-lav"),
        card(430,176,252,88,"Stoffel::compile","source to runtime handle","card card-cream"),
        card(430,326,252,88,"Stoffel::load_file","load built .stflb artifact","card card-cream"),
        card(824,162,258,88,"execute_clear()","fast local logic check","card card-cyan"),
        card(824,298,258,88,"execute_local().await","spawn local MPC parties","card card-blue"),
        card(824,438,258,78,"network handles","deployment/server/client config","card card-cyan"),
        curve("M304,265 L360,265 L360,220 L430,220"),
        curve("M304,265 L360,265 L360,370 L430,370"),
        curve("M682,220 L742,220 L742,206 L824,206"),
        curve("M682,370 L742,370 L742,342 L824,342"),
        curve("M682,370 L742,370 L742,477 L824,477", "arrow-soft"),
        curve("M953,386 C920,552 240,552 191,310", "arrow-soft"),
        chip(466,535,268,"authorized outputs return to app"),
    ])
    return Diagram("rust-sdk-runtime-paths", "Rust SDK runtime paths", "One API surface for compile/load, clear checks, local MPC, and deployment wiring", body)


def vm_model() -> Diagram:
    body="\n".join([
        zone(44,140,270,386,"Program artifact"),
        zone(360,140,470,386,"Stoffel VM core"),
        zone(884,140,272,386,"MPC hooks"),
        card(84,246,190,78,".stflb bytecode","functions + constants","card card-cream"),
        card(430,184,330,78,"instruction dispatcher","program counter + opcodes","card card-lav"),
        card(430,308,156,82,"clear registers","public values","card card-cyan"),
        card(604,308,156,82,"secret registers","share values","card card-blue"),
        card(430,438,330,62,"runtime state stores","objects, arrays, closures","card card-lav"),
        card(920,214,200,78,"protocol builtins","share ops + reveal","card card-cream"),
        card(920,360,200,78,"network parties","rounds for secret×secret","card card-cream"),
        '<path d="M836,188 L836,466" class="boundary"/>',
        chip(778,166,116,"MPC gate"),
        curve("M274,285 L430,223"),
        curve("M595,262 L595,286 L508,308"),
        curve("M595,262 L595,286 L682,308"),
        curve("M508,390 L508,438", "arrow-soft"),
        curve("M682,390 L682,438", "arrow-soft"),
        curve("M682,390 L682,410 L836,410 L836,253 L920,253"),
        arrow(1020,292,1020,360,"arrow-soft"),
    ])
    return Diagram("vm-execution-model", "Stoffel VM execution model", "Bytecode drives clear registers, secret registers, builtins, and protocol hooks", body)


def honeybadger() -> Diagram:
    body="\n".join([
        zone(54,136,282,374,"Client/app side"),
        zone(410,136,380,374,"Coordination + preprocessing"),
        zone(864,136,286,374,"Party mesh"),
        card(90,206,206,76,"input client","submits protected inputs","card card-lav"),
        card(90,348,206,76,"output client","receives output shares","card card-lav"),
        card(456,184,288,78,"coordinator","reservations, sessions, IO routing","card card-cyan"),
        card(456,326,288,82,"preprocessing","Beaver triples + random shares","card card-cream"),
        card(900,190,98,72,"P1","VM","card card-blue"),
        card(1018,190,98,72,"P2","VM","card card-blue"),
        card(959,338,98,72,"Pn","VM","card card-blue"),
        arrow(296,244,456,223),
        curve("M744,223 L816,223 L816,226 L900,226"),
        curve("M744,367 L830,367 L830,374 L959,374"),
        curve("M998,226 C1012,180 1032,180 1067,226","arrow-dash"),
        curve("M949,262 C930,302 938,328 988,338","arrow-dash"),
        curve("M1067,338 C1122,316 1132,258 1116,226","arrow-dash"),
        curve("M1008,410 C894,548 262,548 193,424", "arrow-soft"),
        chip(458,532,258,"output shares return to authorized clients"),
        chip(796,176,92,"load .stflb"), chip(792,344,96,"triples"),
    ])
    return Diagram("honeybadger-network", "HoneyBadger MPC runtime", "Coordinator-managed sessions with preprocessing and peer protocol rounds", body)


def why_stoffel_dev_gap() -> Diagram:
    body = "\n".join([
        zone(54, 136, 492, 386, "Traditional MPC project"),
        zone(654, 136, 492, 386, "Stoffel project"),
        card(92, 202, 170, 82, "protocol study", "paper + proofs", "card card-cream"),
        card(318, 202, 170, 82, "custom stack", "crypto + networking", "card card-cream"),
        card(206, 356, 170, 82, "late app test", "integration after plumbing", "card card-cream"),
        arrow(262, 243, 318, 243),
        curve("M403,284 C408,330 350,350 291,365", "arrow-soft"),
        chip(174, 476, 252, "specialized plumbing first"),
        card(698, 202, 150, 82, ".stfl logic", "app computation", "card card-lav"),
        card(890, 202, 150, 82, "check + build", ".stflb artifact", "card card-cream"),
        card(794, 356, 150, 82, "local MPC", "party smoke test", "card card-blue"),
        card(980, 356, 130, 82, "Rust SDK", "app boundary", "card card-cyan"),
        arrow(848, 243, 890, 243),
        curve("M965,284 C970,330 900,350 870,356", "arrow-soft"),
        arrow(944, 397, 980, 397),
        chip(780, 476, 272, "application iteration stays visible"),
    ])
    return Diagram("why-stoffel-dev-gap", "From protocol project to app workflow", "Stoffel moves MPC work from bespoke plumbing into a repeatable developer loop", body)


def why_stoffel_toolchain() -> Diagram:
    labels = [
        (78, "StoffelLang", "model secret values", "card card-lav"),
        (284, "CLI", "init, check, build, run", "card card-cream"),
        (490, ".stflb", "bytecode + manifest", "card card-cream"),
        (696, "VM parties", "compute over shares", "card card-blue"),
        (902, "Rust SDK", "application integration", "card card-cyan"),
    ]
    parts = []
    for x, title, sub, cls in labels:
        parts.append(card(x, 232, 160, 92, title, sub, cls))
    for (x, *_), (nx, *__) in zip(labels, labels[1:]):
        parts.append(arrow(x + 160, 278, nx, 278))
    parts += [
        card(154, 420, 230, 74, "clear checks", "fast logic feedback", "card card-lav"),
        card(486, 420, 230, 74, "local MPC tests", "parties + threshold", "card card-blue"),
        card(818, 420, 230, 74, "deployment planning", "network/config boundaries", "card card-cyan"),
        arrow(384, 457, 486, 457),
        arrow(716, 457, 818, 457),
        chip(424, 154, 352, "one artifact connects language, runtime, and app code"),
    ]
    return Diagram("why-stoffel-toolchain", "Stoffel toolchain advantage", "A language, compiler, VM, CLI, and SDK share one bytecode contract", "\n".join(parts))


def why_stoffel_privacy_boundary() -> Diagram:
    body = "\n".join([
        zone(58, 140, 486, 374, "Conventional backend"),
        zone(656, 140, 486, 374, "Stoffel-backed workflow"),
        card(96, 214, 162, 80, "private input", "arrives as plaintext", "card card-lav"),
        card(332, 214, 162, 80, "service logic", "can log or inspect", "card card-cream"),
        card(214, 382, 162, 80, "database/logs", "retain sensitive traces", "card card-cream"),
        arrow(258, 254, 332, 254),
        curve("M413,294 C414,346 330,366 295,382", "arrow-soft"),
        card(694, 206, 148, 78, "client shares", "raw value split", "card card-lav"),
        card(886, 206, 148, 78, "MPC parties", "VM over shares", "card card-blue"),
        card(790, 376, 190, 82, "authorized output", "only explicit reveal/send", "card card-cyan"),
        arrow(842, 245, 886, 245),
        curve("M960,284 C970,332 930,354 885,376", "arrow-soft"),
        chip(716, 500, 360, "privacy boundary is part of the program shape"),
    ])
    return Diagram("why-stoffel-privacy-boundary", "Privacy boundary comparison", "Stoffel keeps private inputs in shares until the program explicitly opens or sends output", body)


def write_all() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    system_flow = stack()
    diagrams = [
        system_flow,
        Diagram("stoffel-stack-introduction", system_flow.title, system_flow.subtitle, system_flow.body),
        mpc_flow(),
        dev_loop(),
        compilation(),
        sdk_paths(),
        vm_model(),
        honeybadger(),
        why_stoffel_dev_gap(),
        why_stoffel_toolchain(),
        why_stoffel_privacy_boundary(),
    ]
    qa = {
        "diagrams": [],
        "xml_parse_errors": [],
        "missing_title_or_desc": [],
        "dimension_issues": [],
        "contrast": contrast_qa(),
        "layout": [],
        "layout_issues": [],
    }
    for d in diagrams:
        path = OUT_DIR / f"{d.name}.svg"
        path.write_text(base(d), encoding="utf-8")
        try:
            root = ET.parse(path).getroot()
            if root.attrib.get("width") != str(W) or root.attrib.get("height") != str(H):
                qa["dimension_issues"].append(str(path))
            ns = "{http://www.w3.org/2000/svg}"
            if root.find(ns + "title") is None or root.find(ns + "desc") is None:
                qa["missing_title_or_desc"].append(str(path))
            layout = layout_qa_for_svg(root, d.name)
            qa["layout"].append(layout)
            qa["layout_issues"].extend(layout["issues"])
        except Exception as exc:
            qa["xml_parse_errors"].append({"path": str(path), "error": str(exc)})
        qa["diagrams"].append({"path": str(path), "width": W, "height": H})
    QA_PATH.write_text(json.dumps(qa, indent=2), encoding="utf-8")
    return qa

if __name__ == "__main__":
    result = write_all()
    print(json.dumps({
        "diagram_count": len(result["diagrams"]),
        "xml_parse_error_count": len(result["xml_parse_errors"]),
        "missing_title_or_desc_count": len(result["missing_title_or_desc"]),
        "dimension_issue_count": len(result["dimension_issues"]),
        "contrast_issue_count": len(result["contrast"]["issues"]),
        "layout_issue_count": len(result["layout_issues"]),
        "qa_path": str(QA_PATH),
    }, indent=2))
