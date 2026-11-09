"""Print the board outline's bounding-box center for KiCad --user-origin."""

import sys

import pcbnew


def main():
    board = pcbnew.LoadBoard(sys.argv[1])
    outline = pcbnew.SHAPE_POLY_SET()
    if not board.GetBoardPolygonOutlines(outline, False):
        raise SystemExit("Cannot center export: missing or invalid Edge.Cuts outline")
    bounds = outline.BBox()
    x = pcbnew.ToMM(bounds.GetX()) + pcbnew.ToMM(bounds.GetWidth()) / 2
    y = pcbnew.ToMM(bounds.GetY()) + pcbnew.ToMM(bounds.GetHeight()) / 2
    print(f"{x:.6f}x{y:.6f}mm")


if __name__ == "__main__":
    main()
