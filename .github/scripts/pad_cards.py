"""Add a transparent right gutter to the three floated profile cards."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
OUTPUT = ROOT / "assets" / "cards"
OUTPUT.mkdir(parents=True, exist_ok=True)

for name in ("languages", "repositories", "repository-ownership"):
    card = ET.parse(ROOT / "dist" / f"{name}.svg").getroot()
    width, height = float(card.attrib["width"]), float(card.attrib["height"])
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid dimensions for {name}")
    # Padding is part of the image, so README CSS cannot remove the gap.
    canvas = ET.Element(f"{{{SVG}}}svg", {
        "width": f"{width + 32:g}", "height": f"{height:g}",
        "viewBox": f"0 0 {width + 32:g} {height:g}", "role": "img",
    })
    card.set("x", "0")
    card.set("y", "0")
    canvas.append(card)
    ET.ElementTree(canvas).write(OUTPUT / f"{name}.svg", encoding="utf-8", xml_declaration=True)
