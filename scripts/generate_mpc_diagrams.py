#!/usr/bin/env python3
"""Generate source-grounded MPC diagrams and deterministic QA metadata."""

from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "diagrams"
QA = ROOT / "scripts" / "mpc-diagram-qa.json"

W, H = 1200, 675

CSS = """
  .bg { fill: #f7f7fa; }
  .header { fill: #2246d2; }
  .zone { fill: #ffffff; stroke: #7f8bb3; stroke-width: 2; stroke-dasharray: 8 7; }
  .card { fill: #ffffff; stroke: #b8bfd5; stroke-width: 2; }
  .private { fill: #fff4d6; stroke: #d89a16; stroke-width: 2; }
  .party { fill: #2246d2; stroke: #15319b; stroke-width: 2; }
  .output { fill: #e9f7f2; stroke: #16836d; stroke-width: 2; }
  .title { font: 700 28px Arial, sans-serif; fill: #ffffff; }
  .subtitle { font: 400 15px Arial, sans-serif; fill: #e9edff; }
  .zone-title { font: 700 17px Arial, sans-serif; fill: #111827; }
  .body { font: 600 15px Arial, sans-serif; fill: #111827; }
  .small { font: 400 13px Arial, sans-serif; fill: #4b5563; }
  .party-title { font: 700 15px Arial, sans-serif; fill: #ffffff; }
  .party-sub { font: 400 12px Arial, sans-serif; fill: #ffffff; }
  .label { font: 700 12px Arial, sans-serif; fill: #31416f; }
  .arrow { fill: none; stroke: #172554; stroke-width: 3; marker-end: url(#arrow); }
  .share-arrow { fill: none; stroke: #2246d2; stroke-width: 2.5; marker-end: url(#blue-arrow); }
"""


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x: int, y: int, value: str, cls: str, anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x: int, y: int, w: int, h: int, cls: str, rx: int = 14) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'


def svg_document(body: str, title: str, description: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(description)}</desc>
<defs>
  <style>{CSS}</style>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#172554"/></marker>
  <marker id="blue-arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#2246d2"/></marker>
</defs>
{body}
</svg>
'''


def privacy_flow() -> str:
    parts = [
        rect(0, 0, W, H, "bg", 0),
        rect(0, 0, W, 92, "header", 0),
        text(52, 42, "Private computation boundary", "title"),
        text(52, 70, "Parties hold shares; only an explicitly authorized output leaves", "subtitle"),
        rect(52, 126, 244, 464, "zone"),
        text(76, 158, "Input owners", "zone-title"),
        rect(76, 188, 196, 100, "private"),
        text(174, 226, "Alice", "body", "middle"),
        text(174, 254, "private value x", "small", "middle"),
        rect(76, 330, 196, 100, "private"),
        text(174, 368, "Bob", "body", "middle"),
        text(174, 396, "private value y", "small", "middle"),
        text(174, 482, "Prepare one share", "body", "middle"),
        text(174, 506, "for each MPC party", "small", "middle"),
        rect(354, 126, 522, 464, "zone"),
        text(378, 158, "Private-computation boundary", "zone-title"),
        rect(392, 180, 446, 46, "card"),
        text(615, 209, "Each party receives its indexed shares — never complete x or y", "label", "middle"),
        rect(392, 250, 138, 116, "party"),
        text(461, 287, "Party 1", "party-title", "middle"),
        text(461, 314, "holds x₁, y₁", "party-sub", "middle"),
        text(461, 339, "computes on shares", "party-sub", "middle"),
        rect(546, 250, 138, 116, "party"),
        text(615, 287, "Party 2", "party-title", "middle"),
        text(615, 314, "holds x₂, y₂", "party-sub", "middle"),
        text(615, 339, "computes on shares", "party-sub", "middle"),
        rect(700, 250, 138, 116, "party"),
        text(769, 287, "Party n", "party-title", "middle"),
        text(769, 314, "holds xₙ, yₙ", "party-sub", "middle"),
        text(769, 339, "computes on shares", "party-sub", "middle"),
        text(615, 394, "Party-to-party protocol messages", "body", "middle"),
        '<path d="M460 406 C510 458, 565 458, 615 406" class="share-arrow"/>',
        '<path d="M615 406 C665 458, 720 458, 770 406" class="share-arrow"/>',
        rect(392, 468, 446, 82, "card"),
        text(615, 500, "Private inputs and intermediate values stay shared", "body", "middle"),
        text(615, 528, "They are not reconstructed as outputs", "small", "middle"),
        rect(934, 208, 214, 194, "output"),
        text(1041, 245, "Authorized recipient", "zone-title", "middle"),
        text(1041, 282, "explicit opening", "body", "middle"),
        text(1041, 307, "or client-output shares", "body", "middle"),
        text(1041, 349, "Only the declared", "small", "middle"),
        text(1041, 372, "output crosses the boundary", "small", "middle"),
        '<path d="M876 292 L922 292" class="arrow"/>',
        text(899, 274, "authorized output", "label", "middle"),
        '<path d="M296 238 L380 200" class="arrow"/>',
        '<path d="M296 380 L380 214" class="arrow"/>',
        text(332, 207, "share sets", "label", "middle"),
        text(329, 323, "share sets", "label", "middle"),
    ]
    return svg_document(
        "\n".join(parts),
        "Private computation boundary",
        "Alice and Bob prepare a share for each MPC party. Parties hold only shares and exchange protocol messages. Private inputs and intermediate values remain shared. Only an explicitly authorized opened result or client-output shares leave the boundary.",
    )


def validate_svg(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    title = root.find("{http://www.w3.org/2000/svg}title")
    desc = root.find("{http://www.w3.org/2000/svg}desc")
    return {
        "path": str(path.relative_to(ROOT)),
        "width": width,
        "height": height,
        "dimension_ok": [width, height] == [W, H],
        "xml_ok": True,
        "accessible_title": bool(title is not None and title.text),
        "accessible_description": bool(desc is not None and desc.text),
        "semantic_checks": {
            "parties_named_as_parties": all(token in path.read_text() for token in ["Party 1", "Party 2", "Party n"]),
            "party_share_ownership_shown": all(token in path.read_text() for token in ["holds x₁, y₁", "holds x₂, y₂", "holds xₙ, yₙ"]),
            "private_state_stays_inside_boundary": "Private inputs and intermediate values stay shared" in path.read_text(),
            "authorized_output_only": "Only the declared" in path.read_text(),
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {OUT / "mpc-privacy-flow.svg": privacy_flow()}
    for path, content in outputs.items():
        path.write_text(content)
    report = {"generator": str(Path(__file__).relative_to(ROOT)), "outputs": [validate_svg(path) for path in outputs]}
    QA.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
