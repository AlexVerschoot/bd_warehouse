"""
Aluminum extrusions

name: aluminum_extrusions.py
by:   Alex Verschoot
date: December 27, 2025

desc:
    This python module is a CAD library of parametric aluminum extrions. 
    They are mostly based on manufacturer provided data.

"""

from build123d import Align, BaseSketchObject, BuildLine, BuildSketch, Literal, Location, Locations, Mode, Plane, Polyline, RectangleRounded, FilletPolyline, make_face, mirror
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
            name, width, height, corner_radius, hole_dia, flange_thickness, flange_opening, flange_max_width, flange_depth, flange_bottom_radius, flange_neck_top_radius, flange_neck_bottom_radius, flange_top_radius, source = row

            extrusionData[name] = {}
            extrusionData[name]['width'] = float(width)
            extrusionData[name]['height'] = float(height)
            extrusionData[name]['corner_radius'] = float(corner_radius)
            extrusionData[name]['hole_dia'] = float(hole_dia)
            extrusionData[name]['flange_thickness'] = float(flange_thickness)
            extrusionData[name]['flange_opening'] = float(flange_opening)
            extrusionData[name]['flange_max_width'] = float(flange_max_width)
            extrusionData[name]['flange_depth'] = float(flange_depth)
            extrusionData[name]['flange_bottom_radius'] = float(flange_bottom_radius)
            extrusionData[name]['flange_neck_top_radius'] = float(flange_neck_top_radius)
            extrusionData[name]['flange_neck_bottom_radius'] = float(flange_neck_bottom_radius)
            extrusionData[name]['flange_top_radius'] = float(flange_top_radius)
            extrusionData[name]['source'] = source


    def __init__(
        self,
        extrusion_type: str = "Item24 Profile 5 20x20",
        rotation: float = 0,
        align: tuple[Align, Align] = (Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        #_applies_to = [BuildSketch._tag]
        with BuildSketch() as mainSketch:
            #base rectangle
            RectangleRounded(
                width=self.extrusionData[extrusion_type]['width'],
                height=self.extrusionData[extrusion_type]['height'],
                radius=self.extrusionData[extrusion_type]['corner_radius']
            )
            groove_placements = [
                ((0, -self.extrusionData[extrusion_type]['height'] / 2), 0),
                ((0,  self.extrusionData[extrusion_type]['height'] / 2), 180),
                ((-self.extrusionData[extrusion_type]['width'] / 2, 0), -90),
                (( self.extrusionData[extrusion_type]['width'] / 2, 0), 90),
            ]
            for (x, y), rot in groove_placements:
                with BuildLine(Location((x,y,0),angle=rot)) as grooves:
                    slot_groove_points = [
                        #extra start in line with the profile to make easy entry fillet
                        (self.extrusionData[extrusion_type]['flange_opening']*3/4, -1),
                        (self.extrusionData[extrusion_type]['flange_opening']*3/4, 0),
                        #the real figure starts
                        (self.extrusionData[extrusion_type]['flange_opening']/2, 0),
                        (self.extrusionData[extrusion_type]['flange_opening']/2, self.extrusionData[extrusion_type]['flange_thickness']),
                        (self.extrusionData[extrusion_type]['flange_max_width']/2, self.extrusionData[extrusion_type]['flange_thickness']),
                        (self.extrusionData[extrusion_type]['flange_opening']/2, self.extrusionData[extrusion_type]['flange_depth']),
                        #(0, self.extrusionData[extrusion_type]['flange_depth']),
                        (-self.extrusionData[extrusion_type]['flange_opening']/2, self.extrusionData[extrusion_type]['flange_depth']),
                        (-self.extrusionData[extrusion_type]['flange_max_width']/2, self.extrusionData[extrusion_type]['flange_thickness']),
                        (-self.extrusionData[extrusion_type]['flange_opening']/2, self.extrusionData[extrusion_type]['flange_thickness']),
                        (-self.extrusionData[extrusion_type]['flange_opening']/2, 0),
                        #the real figure ends
                        (-self.extrusionData[extrusion_type]['flange_opening']*3/4, 0),
                        (-self.extrusionData[extrusion_type]['flange_opening']*3/4, -1),

                    ]
                    slot_groove_radii = [
                        0,
                        0,
                        self.extrusionData[extrusion_type]['flange_neck_top_radius'],
                        self.extrusionData[extrusion_type]['flange_neck_bottom_radius'],
                        self.extrusionData[extrusion_type]['flange_top_radius'],
                        self.extrusionData[extrusion_type]['flange_bottom_radius'],
                        self.extrusionData[extrusion_type]['flange_bottom_radius'],
                        self.extrusionData[extrusion_type]['flange_top_radius'],
                        self.extrusionData[extrusion_type]['flange_neck_bottom_radius'],
                        self.extrusionData[extrusion_type]['flange_neck_top_radius'],
                        0,
                        0
                    ]
                    fpl = FilletPolyline(slot_groove_points, radius=slot_groove_radii, close=True, mode=Mode.ADD)
                make_face(edges=grooves.edges(), mode=Mode.SUBTRACT)
        
        super().__init__(obj=mainSketch.sketch, rotation=rotation, align=align, mode=mode)


if __name__ == "__main__":
    from ocp_vscode import *

    a = AluminiumExtrusionIType()
    show_all()