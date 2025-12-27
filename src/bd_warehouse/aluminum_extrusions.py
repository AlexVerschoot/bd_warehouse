"""
Aluminum extrusions

name: aluminum_extrusions.py
by:   Alex Verschoot
date: December 27, 2025

desc:
    This python module is a CAD library of parametric aluminum extrions. 
    They are mostly based on manufacturer provided data.

"""

from build123d import Align, BaseSketchObject, BuildLine, BuildSketch, Literal, Mode, RectangleRounded, FilletPolyline
import csv
import importlib.resources as pkg_resources
import bd_warehouse


class AluminiumExtrusionIType(BaseSketchObject):
    extrusionData = {}
    with pkg_resources.open_text(bd_warehouse, "data/aluminum_extrusions_I_type.csv") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the header row
        for row in reader:
            if len(row) == 0:  # skip blank rows
                continue
            name, width,height,corner_radius,hole_dia,flange_thickness,flange_opening,flange_depth,source = row
            extrusionData[name] = {}
            extrusionData[name]['width'] = float(width)
            extrusionData[name]['height'] = float(height)
            extrusionData[name]['corner_radius'] = float(corner_radius)
            extrusionData[name]['hole_dia'] = float(hole_dia)
            extrusionData[name]['flange_thickness'] = float(flange_thickness)
            extrusionData[name]['flange_opening'] = float(flange_opening)
            extrusionData[name]['flange_depth'] = float(flange_depth)

    def __init__(
        self,
        extrusion_type: str = "Item24 Profile 5 20x20",
        rotation: float = 0,
        align: tuple[Align, Align] = (Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        _applies_to = [BuildSketch._tag]
        with BuildSketch() as mainSketch:
            RectangleRounded(
                width=self.extrusionData[extrusion_type]['width'],
                height=self.extrusionData[extrusion_type]['height'],
                radius=self.extrusionData[extrusion_type]['corner_radius']
            )
            
        
        super().__init__(obj=mainSketch.sketch, rotation=rotation, align=align, mode=mode)


if __name__ == "__main__":
    from ocp_vscode import *

    a = AluminiumExtrusionIType()
    show_all()