"""Export copper-layer PDFs and dimensions using the installed KiCad Python API."""

import os
from pathlib import Path
import subprocess
import sys

import pcbnew


def main():
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)
    board = pcbnew.LoadBoard(str(source))
    layers = [board.GetLayerName(layer) for layer in board.GetEnabledLayers().CuStack()]

    outline = pcbnew.SHAPE_POLY_SET()
    if board.GetBoardPolygonOutlines(outline, False):
        bounds = outline.BBox()
        dimensions = (
            f"{pcbnew.ToMM(bounds.GetWidth()):.3f} × "
            f"{pcbnew.ToMM(bounds.GetHeight()):.3f} mm"
        )
    else:
        dimensions = "Unavailable: missing or invalid Edge.Cuts outline"

    thickness = pcbnew.ToMM(board.GetDesignSettings().GetBoardThickness())
    report = (
        f"### {source.stem}\n\n"
        f"- Outline width × height: {dimensions}\n"
        f"- Configured board thickness: {thickness:.3f} mm\n"
        f"- Copper layers, top to bottom: {', '.join(layers)}\n\n"
        "Dimensions use the axis-aligned board outline bounds, excluding components.\n"
    )
    (output / f"{source.stem}-dimensions.md").write_text(report)
    print(report, flush=True)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write(report + "\n")

    subprocess.run(
        [
            "kicad-cli", "pcb", "export", "pdf",
            "--layers", ",".join(layers),
            "--common-layers", "Edge.Cuts",
            "--mode-multipage",
            "--include-border-title",
            "--black-and-white",
            "--scale", "0",
            "--check-zones",
            "--output", str(output / f"{source.stem}-copper.pdf"),
            str(source),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
