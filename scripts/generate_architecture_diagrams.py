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
.subtitle { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 17px; font-weight: 400; fill: #dfe4ff; }
.zone { fill: #ffffff; stroke: #b8bde8; stroke-width: 2; stroke-dasharray: 9 8; rx: 22; }
.zone-title { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 17px; font-weight: 700; fill: #17214f; letter-spacing: .02em; }
.card { fill: #ffffff; stroke: #c6cbef; stroke-width: 2; rx: 16; }
.card-lav { fill: #ebe9ff; stroke: #c6c0ff; }
.card-cream { fill: #fff6df; stroke: #edd797; }
.card-blue { fill: #3448f0; stroke: #2335c8; }
.card-cyan { fill: #e5fbff; stroke: #7be4f5; }
.card-text { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 18px; font-weight: 700; fill: #121a44; }
.card-sub { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 14px; font-weight: 400; fill: #465078; }
.white { fill: #ffffff; }
.on-blue-title { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 18px; font-weight: 700; fill: #ffffff; }
.on-blue-sub { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 14px; font-weight: 400; fill: #ffffff; opacity: .95; }
.small { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 13px; font-weight: 400; fill: #465078; }
.badge { fill: #5ee3ff; stroke: #28bfdc; stroke-width: 1.5; }
.badge-text { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 15px; font-weight: 700; fill: #07133d; text-anchor: middle; dominant-baseline: middle; }
.arrow { stroke: #101a45; stroke-width: 3; fill: none; marker-end: url(#arrow); stroke-linecap: round; stroke-linejoin: round; }
.arrow-soft { stroke: #3448f0; stroke-width: 2.5; fill: none; marker-end: url(#arrow-soft); stroke-linecap: round; stroke-linejoin: round; opacity: .85; }
.arrow-dash { stroke: #3448f0; stroke-width: 2.5; fill: none; stroke-dasharray: 7 7; marker-end: url(#arrow-soft); opacity: .72; }
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
    "card-cyan": "#e5fbff",
    "zone": "#ffffff",
    "label-chip": "#ffffff",
    "badge": "#5ee3ff",
}

TEXT_COLORS = {
    "title": "#ffffff",
    "subtitle": "#dfe4ff",
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
        out.append(f'<text x="{x}" y="{y + i * gap}" class="{cls}" text-anchor="{anchor}">{esc(line)}</text>')
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
  <text x="48" y="68" class="subtitle">{esc(diagram.subtitle)}</text>
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
    ])
    return Diagram("stoffel-stack", "Stoffel system flow", "Source, build artifact, runtime parties, and authorized outputs", body)


def mpc_flow() -> Diagram:
    body = "\n".join([
        zone(62, 128, 292, 382, "Input owners"), zone(454, 128, 292, 382, "MPC parties"), zone(846, 128, 292, 382, "Authorized output"),
        card(98, 188, 220, 74, "Alice input", "raw value stays private", "card card-lav"),
        card(98, 306, 220, 74, "Bob input", "raw value stays private", "card card-lav"),
        card(486, 178, 228, 70, "share 1", "one masked fragment", "card card-blue"),
        card(486, 286, 228, 70, "share 2", "one masked fragment", "card card-blue"),
        card(486, 394, 228, 70, "share n", "one masked fragment", "card card-blue"),
        card(886, 228, 212, 86, "opened result", "only the value the|program reveals", "card card-cream"),
        card(886, 366, 212, 74, "private trace", "inputs + intermediates|remain secret", "card card-cyan"),
        arrow(318, 224, 486, 213), arrow(318, 224, 486, 321), arrow(318, 224, 486, 429),
        arrow(318, 342, 486, 213), arrow(318, 342, 486, 321), arrow(318, 342, 486, 429),
        curve("M714,213 C785,220 810,238 886,270"), curve("M714,321 C795,320 815,306 886,286"), curve("M714,429 C800,420 825,386 886,403", "arrow-soft"),
        chip(370, 146, 140, "split into shares"), chip(752, 174, 116, "compute"), chip(770, 462, 150, "not reconstructed"),
    ])
    return Diagram("mpc-privacy-flow", "MPC privacy flow", "Inputs are shared, computed over, and revealed only at explicit output boundaries", body)


def dev_loop() -> Diagram:
    steps = [
        (88, 214, "1", "write", "src/main.stfl"),
        (292, 214, "2", "check", "validate source"),
        (496, 214, "3", "build", ".stflb artifact"),
        (700, 214, "4", "run", "local MPC nodes"),
        (904, 214, "5", "integrate", "Rust SDK wrapper"),
    ]
    parts=[]
    for x,y,n,t,s in steps:
        parts.append(f'<circle cx="{x+35}" cy="{y-32}" r="18" class="badge"/><text x="{x+35}" y="{y-32}" class="badge-text">{n}</text>')
        parts.append(card(x,y,160,92,t,s,"card card-lav" if n in {"1","5"} else "card card-cream"))
    for i in range(len(steps)-1): parts.append(arrow(steps[i][0]+160,260,steps[i+1][0],260))
    parts += [
        curve("M984,306 C940,488 210,488 168,306", "arrow-soft"), chip(452, 477, 296, "edit, rebuild, rerun until the boundary is right"),
        card(334, 404, 532, 62, "Local MPC testing spawns several parties on your machine", "use parties + threshold settings from Stoffel.toml or CLI flags", "card card-cyan"),
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
        card(74,180,240,88,"Rust application","domain types + service logic","card card-lav"),
        card(430,150,260,88,"Stoffel::compile","source to runtime handle","card card-cream"),
        card(430,290,260,88,"Stoffel::load_file","load built .stflb artifact","card card-cream"),
        card(816,150,250,88,"execute_clear()","fast local logic check","card card-cyan"),
        card(816,290,250,88,"execute_local().await","spawn local MPC parties","card card-blue"),
        card(816,430,250,78,"network handles","deployment/server/client config","card card-cyan"),
        arrow(314,224,430,194), arrow(314,224,430,334),
        arrow(690,194,816,194), arrow(690,334,816,334), arrow(690,334,816,469,"arrow-soft"),
        curve("M941,378 C910,558 238,558 194,268", "arrow-soft"), chip(474,535,246,"authorized outputs return to app"),
    ])
    return Diagram("rust-sdk-runtime-paths", "Rust SDK runtime paths", "One API surface for compile/load, clear checks, local MPC, and deployment wiring", body)


def vm_model() -> Diagram:
    body="\n".join([
        zone(62,144,260,364,"Program artifact"), zone(392,144,392,364,"Stoffel VM core"), zone(854,144,284,364,"MPC hooks"),
        card(96,220,192,74,".stflb bytecode","functions + constants","card card-cream"),
        card(430,186,316,74,"instruction dispatcher","program counter + opcodes","card card-lav"),
        card(430,292,142,78,"clear registers","public values","card card-cyan"),
        card(604,292,142,78,"secret registers","share values","card card-blue"),
        card(430,414,316,64,"object/array/closure stores","runtime references","card card-lav"),
        card(888,214,216,76,"protocol builtins","share ops + reveal","card card-cream"),
        card(888,340,216,76,"network parties","rounds for secret×secret","card card-cream"),
        arrow(288,257,430,224), arrow(588,260,501,292), arrow(588,260,675,292), arrow(675,370,888,252), arrow(996,290,996,340,"arrow-soft"),
        chip(762,270,108,"MPC boundary"),
    ])
    return Diagram("vm-execution-model", "Stoffel VM execution model", "Bytecode drives clear registers, secret registers, builtins, and protocol hooks", body)


def honeybadger() -> Diagram:
    body="\n".join([
        zone(54,136,272,374,"Client/app side"), zone(410,136,380,374,"Coordination + preprocessing"), zone(870,136,276,374,"Party mesh"),
        card(90,206,200,76,"input client","submits protected inputs","card card-lav"),
        card(90,348,200,76,"output client","receives output shares","card card-lav"),
        card(456,184,288,78,"coordinator","reservations, sessions, IO routing","card card-cyan"),
        card(456,326,288,82,"preprocessing","Beaver triples + random shares","card card-cream"),
        card(900,184,90,70,"P1","VM","card card-blue"),
        card(1020,184,90,70,"P2","VM","card card-blue"),
        card(960,330,90,70,"Pn","VM","card card-blue"),
        arrow(290,244,456,223), arrow(744,223,900,219), arrow(744,367,960,367),
        curve("M990,219 C1010,174 1036,174 1050,219","arrow-dash"), curve("M945,254 C930,292 944,320 985,330","arrow-dash"), curve("M1050,330 C1110,310 1122,245 1110,219","arrow-dash"),
        curve("M960,400 C862,548 260,548 190,424", "arrow-soft"), chip(458,532,258,"output shares return to authorized clients"),
        chip(794,176,86,"load .stflb"), chip(790,344,96,"triples"),
    ])
    return Diagram("honeybadger-network", "HoneyBadger MPC runtime", "Coordinator-managed sessions with preprocessing and peer protocol rounds", body)


def write_all() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diagrams = [stack(), mpc_flow(), dev_loop(), compilation(), sdk_paths(), vm_model(), honeybadger()]
    qa = {
        "diagrams": [],
        "xml_parse_errors": [],
        "missing_title_or_desc": [],
        "dimension_issues": [],
        "contrast": contrast_qa(),
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
        "qa_path": str(QA_PATH),
    }, indent=2))
