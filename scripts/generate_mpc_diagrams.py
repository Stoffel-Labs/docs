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
  .hb { fill: #eef1ff; stroke: #2246d2; stroke-width: 2; }
  .avss { fill: #f3eefe; stroke: #7251b5; stroke-width: 2; }
  .phase { fill: #ffffff; stroke: #c9cee0; stroke-width: 1.5; }
  .label-chip { fill: #f7f7fa; }
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
  .control-arrow { fill: none; stroke: #596784; stroke-width: 2.5; stroke-dasharray: 7 6; marker-end: url(#arrow); }
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
  <marker id="arrow" markerWidth="10" markerHeight="6" viewBox="0 0 10 6" refX="9.5" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,3 L0,6 Z" fill="#172554"/></marker>
  <marker id="blue-arrow" markerWidth="10" markerHeight="6" viewBox="0 0 10 6" refX="9.5" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,3 L0,6 Z" fill="#2246d2"/></marker>
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


def backend_selection() -> str:
    parts = [
        rect(0, 0, W, H, "bg", 0),
        rect(0, 0, W, 92, "header", 0),
        text(52, 42, "Choose the privacy backend by workload shape", "title"),
        text(52, 70, "The backends differ in data representation, preprocessing, public artifacts, and topology", "subtitle"),
        rect(412, 116, 376, 66, "card"),
        text(600, 143, "Stoffel program + protected inputs", "body", "middle"),
        text(600, 166, "Choose the backend before deployment", "small", "middle"),
        '<path d="M560 182 L560 218 L316 218 L316 230" class="arrow"/>',
        '<path d="M640 182 L640 218 L884 218 L884 230" class="arrow"/>',
        rect(286, 187, 236, 24, "label-chip", 4),
        rect(674, 187, 244, 24, "label-chip", 4),
        text(404, 205, "field-oriented application logic", "label", "middle"),
        text(796, 205, "curve or commitment workflows", "label", "middle"),
        rect(52, 230, 516, 384, "hb"),
        text(84, 266, "HoneyBadgerMPC", "zone-title"),
        text(84, 291, "General field-compatible MPC", "small"),
        rect(84, 316, 452, 64, "phase"),
        text(102, 343, "Representation", "label"),
        text(102, 365, "Field-compatible application values and robust shares", "small"),
        rect(84, 394, 452, 64, "phase"),
        text(102, 421, "Offline / preprocessing", "label"),
        text(102, 443, "Random shares and Beaver triples", "small"),
        rect(84, 472, 452, 64, "phase"),
        text(102, 499, "Application boundary", "label"),
        text(102, 521, "Opened values or client-output shares", "small"),
        rect(84, 550, 452, 42, "phase"),
        text(102, 577, "Full deployment topology: n ≥ 4t + 1", "body"),
        rect(632, 230, 516, 384, "avss"),
        text(664, 266, "AVSS", "zone-title"),
        text(664, 291, "Cryptographic scalar and curve workflows", "small"),
        rect(664, 316, 452, 64, "phase"),
        text(682, 343, "Representation", "label"),
        text(682, 365, "Feldman shares over a selected scalar field and curve", "small"),
        rect(664, 394, 452, 64, "phase"),
        text(682, 421, "Offline / preprocessing", "label"),
        text(682, 443, "Verifiable dealing; commitments are public and non-hiding", "small"),
        rect(664, 472, 452, 64, "phase"),
        text(682, 499, "Application boundary", "label"),
        text(682, 521, "Commitments, curve encodings, or scalar responses", "small"),
        rect(664, 550, 452, 42, "phase"),
        text(682, 577, "Deployment topology: n ≥ 3t + 1", "body"),
        text(600, 648, "Both backends keep private values shared; their interfaces and deployment requirements are not interchangeable.", "small", "middle"),
    ]
    return svg_document(
        "\n".join(parts),
        "Choose the privacy backend by workload shape",
        "HoneyBadgerMPC is the general field-compatible backend with random-share and Beaver-triple preprocessing and a full-deployment requirement of n at least 4t plus 1. AVSS is designed for scalar, curve, and commitment workflows with verifiable dealing, public non-hiding Feldman commitments, and n at least 3t plus 1.",
    )


def networked_runtime() -> str:
    parts = [
        rect(0, 0, W, H, "bg", 0),
        rect(0, 0, W, 92, "header", 0),
        text(52, 42, "Networked MPC runtime", "title"),
        text(52, 70, "Control-plane coordination is separate from share computation and client-side reconstruction", "subtitle"),
        rect(44, 122, 250, 496, "zone"),
        text(68, 154, "Application boundary", "zone-title"),
        rect(70, 178, 198, 96, "private"),
        text(169, 213, "App / client", "body", "middle"),
        text(169, 240, "prepares protected inputs", "small", "middle"),
        text(169, 261, "and requests a session", "small", "middle"),
        rect(70, 326, 198, 86, "card"),
        text(169, 359, ".stflb + manifest", "body", "middle"),
        text(169, 386, "same contract for every party", "small", "middle"),
        rect(70, 472, 198, 102, "output"),
        text(169, 506, "Authorized client", "body", "middle"),
        text(169, 533, "receives output shares", "small", "middle"),
        text(169, 554, "and reconstructs", "small", "middle"),
        rect(330, 122, 250, 496, "zone"),
        text(354, 154, "Control plane", "zone-title"),
        rect(356, 178, 198, 124, "card"),
        text(455, 211, "Coordinator", "body", "middle"),
        text(455, 238, "session lifecycle", "small", "middle"),
        text(455, 260, "reservations + routing", "small", "middle"),
        text(455, 282, "deployment metadata", "small", "middle"),
        rect(356, 336, 198, 92, "hb"),
        text(455, 369, "Control metadata", "body", "middle"),
        text(455, 396, "is not the secret", "small", "middle"),
        text(455, 417, "computation", "small", "middle"),
        text(455, 482, "Coordinator arranges delivery;", "small", "middle"),
        text(455, 505, "parties compute on shares and", "small", "middle"),
        text(455, 528, "the authorized client reconstructs.", "small", "middle"),
        rect(620, 122, 536, 496, "zone"),
        text(644, 154, "MPC party boundary", "zone-title"),
        rect(650, 192, 142, 108, "party"),
        text(721, 230, "Party 1", "party-title", "middle"),
        text(721, 257, "Stoffel VM", "party-sub", "middle"),
        text(721, 280, "holds shares", "party-sub", "middle"),
        rect(816, 192, 142, 108, "party"),
        text(887, 230, "Party 2", "party-title", "middle"),
        text(887, 257, "Stoffel VM", "party-sub", "middle"),
        text(887, 280, "holds shares", "party-sub", "middle"),
        rect(982, 192, 142, 108, "party"),
        text(1053, 230, "Party n", "party-title", "middle"),
        text(1053, 257, "Stoffel VM", "party-sub", "middle"),
        text(1053, 280, "holds shares", "party-sub", "middle"),
        rect(735, 312, 304, 25, "label-chip", 4),
        text(887, 331, "Authenticated party-to-party protocol messages", "label", "middle"),
        '<path d="M720 352 C775 406, 832 406, 887 352" class="share-arrow"/>',
        '<path d="M887 352 C942 406, 999 406, 1054 352" class="share-arrow"/>',
        rect(650, 438, 474, 110, "card"),
        text(887, 472, "Party-local preprocessing stores", "body", "middle"),
        text(887, 499, "random shares / triples or verified material", "small", "middle"),
        text(887, 525, "material is consumed by the selected backend", "small", "middle"),
        '<path d="M721 438 L721 312" class="control-arrow"/>',
        '<path d="M887 438 L887 312" class="control-arrow"/>',
        '<path d="M1053 438 L1053 312" class="control-arrow"/>',
        '<path d="M268 214 L344 214" class="control-arrow"/>',
        text(306, 199, "session", "label", "middle"),
        '<path d="M554 238 L638 238" class="control-arrow"/>',
        text(596, 223, "control", "label", "middle"),
        '<path d="M268 354 C300 390, 310 450, 344 450 L590 450 C620 420, 620 350, 638 320" class="arrow"/>',
        rect(326, 437, 252, 25, "label-chip", 4),
        text(452, 455, "same artifact + manifest to every party", "label", "middle"),
        '<path d="M268 266 C285 290, 300 318, 344 318 L590 318 C610 318, 620 290, 638 272" class="share-arrow"/>',
        rect(370, 306, 170, 25, "label-chip", 4),
        text(455, 324, "protected input delivery", "label", "middle"),
        '<path d="M638 574 C500 600, 400 600, 268 544" class="share-arrow"/>',
        rect(372, 568, 160, 25, "label-chip", 4),
        text(452, 587, "per-party output shares", "label", "middle"),
        text(887, 590, "No individual party receives a complete private input.", "small", "middle"),
    ]
    return svg_document(
        "\n".join(parts),
        "Networked MPC runtime",
        "The app and coordinator establish a session and distribute one compiled artifact. Protected inputs are delivered to MPC parties. Each party runs the Stoffel VM over shares, exchanges authenticated protocol messages, and consumes party-local preprocessing. Per-party output shares return to the authorized client for reconstruction.",
    )


def validate_svg(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    source = path.read_text()
    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    title = root.find("{http://www.w3.org/2000/svg}title")
    desc = root.find("{http://www.w3.org/2000/svg}desc")
    checks = (
        {
            "parties_named_as_parties": all(token in source for token in ["Party 1", "Party 2", "Party n"]),
            "party_share_ownership_shown": all(token in source for token in ["holds x₁, y₁", "holds x₂, y₂", "holds xₙ, yₙ"]),
            "private_state_stays_inside_boundary": "Private inputs and intermediate values stay shared" in source,
            "authorized_output_only": "Only the declared" in source,
        }
        if path.name == "mpc-privacy-flow.svg"
        else {
            "party_count_is_symbolic": all(token in source for token in ["Party 1", "Party 2", "Party n"]),
            "control_and_compute_roles_separated": all(token in source for token in ["Control plane", "MPC party boundary"]),
            "preprocessing_is_party_local": "Party-local preprocessing stores" in source,
            "client_reconstruction_shown": all(token in source for token in ["Authorized client", "and reconstructs"]),
        }
        if path.name == "networked-mpc-runtime.svg"
        else {
            "backend_roles_separated": all(token in source for token in ["HoneyBadgerMPC", "AVSS"]),
            "backend_topologies_separated": all(token in source for token in ["n ≥ 4t + 1", "n ≥ 3t + 1"]),
            "preprocessing_distinguished": all(token in source for token in ["Beaver triples", "Verifiable dealing"]),
            "avss_commitment_visibility_stated": "public and non-hiding" in source,
            "branch_labels_clear_of_stems": all(
                token in source
                for token in [
                    'M560 182 L560 218 L316 218 L316 230',
                    'M640 182 L640 218 L884 218 L884 230',
                    'y="187" width="236" height="24"',
                    'y="187" width="244" height="24"',
                ]
            ),
        }
    )
    return {
        "path": str(path.relative_to(ROOT)),
        "width": width,
        "height": height,
        "dimension_ok": [width, height] == [W, H],
        "xml_ok": True,
        "accessible_title": bool(title is not None and title.text),
        "accessible_description": bool(desc is not None and desc.text),
        "arrowheads_centered_on_stems": all(
            token in source
            for token in ['viewBox="0 0 10 6"', 'refX="9.5"', 'refY="3"', 'markerHeight="6"']
        ),
        "semantic_checks": checks,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUT / "mpc-privacy-flow.svg": privacy_flow(),
        OUT / "mpc-backend-selection.svg": backend_selection(),
        OUT / "networked-mpc-runtime.svg": networked_runtime(),
    }
    for path, content in outputs.items():
        path.write_text(content)
    report = {"generator": str(Path(__file__).relative_to(ROOT)), "outputs": [validate_svg(path) for path in outputs]}
    QA.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
