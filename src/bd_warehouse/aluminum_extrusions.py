"""
Aluminum extrusions

name: aluminum_extrusions.py
by:   Alex Verschoot
date: December 27, 2025

desc:
    This python module is a CAD library of parametric aluminum extrions. 
    They are mostly based on manufacturer provided data.

"""

from build123d import Align, BasePartObject, BuildLine, BuildPart, BuildSketch, Circle, ExtensionLine, Face, Location, Mode, RectangleRounded, FilletPolyline, RotationLike, extrude, make_face
from build123d import Draft
import csv
import bd_warehouse
import importlib.resources


class AluminiumExtrusionIType(BasePartObject):
    def __init__(
        self,
        length:float,
        extrusion_type: str = "Item24 Profile 5 20x20",
        rotation: RotationLike = (0, 0, 0),
        align: tuple[Align, Align] = (Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as extrusion:
            extrude(to_extrude=self.getExtrusionFace(extrusion_type), amount=length)  # type: ignore
        super().__init__(part=extrusion.part, rotation=rotation, align=align, mode=mode) # type: ignore

    def getExtrusionFace(extrusion_type: str) -> Face:  # type: ignore
        extrusionData = AluminiumExtrusionIType.getExtrusionData()
        with BuildSketch() as mainSketch:
            #base rectangle
            RectangleRounded(
                width=extrusionData[extrusion_type]['width'], # type: ignore
                height=extrusionData[extrusion_type]['height'], # type: ignore
                radius=extrusionData[extrusion_type]['corner_radius'] # type: ignore
            )
            Circle(radius=extrusionData[extrusion_type]['hole_dia']/2, mode=Mode.SUBTRACT) # type: ignore
            groove_placements: list[tuple[tuple[float, float], float]] = [ 
                ((0, -float(extrusionData[extrusion_type]['height']) / 2), 0),
                ((0,  float(extrusionData[extrusion_type]['height']) / 2), 180),
                ((-float(extrusionData[extrusion_type]['width']) / 2, 0), -90),
                (( float(extrusionData[extrusion_type]['width']) / 2, 0), 90),
            ]
            for (x, y), rot in groove_placements: 
                with BuildLine(Location((x,y,0),angle=rot)) as grooves:
                    slot_groove_points: list[tuple[float, float]] = []
                    slot_groove_radii: list[float] = []
                        #extra start in line with the profile to make easy entry fillet
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_opening'])*3/4, -1))
                    slot_groove_radii.append(0)
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_opening'])*3/4, 0))
                    slot_groove_radii.append(0)
                        #the real figure starts
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_opening'])/2, 0))
                    slot_groove_radii.append((float(extrusionData[extrusion_type]['flange_neck_top_radius'])))
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_opening'])/2, float(extrusionData[extrusion_type]['flange_thickness'])))
                    slot_groove_radii.append((float(extrusionData[extrusion_type]['flange_neck_bottom_radius'])))
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_max_width'])/2, float(extrusionData[extrusion_type]['flange_thickness'])))
                    slot_groove_radii.append((float(extrusionData[extrusion_type]['flange_top_radius'])))
                    if (float(extrusionData[extrusion_type]['flange_offset'])>0):
                        slot_groove_points.append((float(extrusionData[extrusion_type]['flange_max_width'])/2, float(extrusionData[extrusion_type]['flange_thickness'])+float(extrusionData[extrusion_type]['flange_offset'])))
                        slot_groove_radii.append(0)
                    slot_groove_points.append((float(extrusionData[extrusion_type]['flange_bottom_width'])/2, float(extrusionData[extrusion_type]['flange_depth'])))
                    slot_groove_radii.append((float(extrusionData[extrusion_type]['flange_bottom_radius'])))
                    if(float(extrusionData[extrusion_type]['flange_notch_width'])>0):
                        slot_groove_points.append((float(extrusionData[extrusion_type]['flange_notch_width'])/2, float(extrusionData[extrusion_type]['flange_depth'])))
                        slot_groove_radii.append(0)
                        slot_groove_points.append((0, float(extrusionData[extrusion_type]['flange_depth'])+float(extrusionData[extrusion_type]['flange_notch_depth'])))
                        slot_groove_radii.append(0)
                        slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_notch_width'])/2, float(extrusionData[extrusion_type]['flange_depth'])))
                        slot_groove_radii.append(0)
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_bottom_width'])/2, float(extrusionData[extrusion_type]['flange_depth'])))
                    slot_groove_radii.append(float(extrusionData[extrusion_type]['flange_bottom_radius']))
                    if (float(extrusionData[extrusion_type]['flange_offset'])>0):
                        slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_max_width'])/2, float(extrusionData[extrusion_type]['flange_thickness'])+float(extrusionData[extrusion_type]['flange_offset'])))
                        slot_groove_radii.append(0)
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_max_width'])/2, float(extrusionData[extrusion_type]['flange_thickness'])))
                    slot_groove_radii.append(float(extrusionData[extrusion_type]['flange_top_radius']))
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_opening'])/2, float(extrusionData[extrusion_type]['flange_thickness'])))
                    slot_groove_radii.append(float(extrusionData[extrusion_type]['flange_neck_bottom_radius']))
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_opening'])/2, 0))
                    #the real figure ends
                    slot_groove_radii.append(float(extrusionData[extrusion_type]['flange_neck_top_radius']))
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_opening'])*3/4, 0))
                    slot_groove_radii.append(0)
                    slot_groove_points.append((-float(extrusionData[extrusion_type]['flange_opening'])*3/4, -1))
                    slot_groove_radii.append(0)
                   
                    FilletPolyline(slot_groove_points, radius=slot_groove_radii, close=True, mode=Mode.ADD)
                make_face(edges=grooves.edges(), mode=Mode.SUBTRACT)
        return mainSketch.face()
    
    def getDimensionedExtrusionFace(extrusion_type:str)->Face:  # type: ignore
        extrusionData = AluminiumExtrusionIType.getExtrusionData()
        extrusion_face = AluminiumExtrusionIType.getExtrusionFace(extrusion_type) # type: ignore
        draft = Draft(font_size=2, extension_gap=0, line_width=0.1, pad_around_text=0.5,)
        width =  ExtensionLine(
                border=((-extrusionData[name]['width']/2, extrusionData[name]['height']/2),(extrusionData[name]['width']/2, extrusionData[name]['height']/2)), # type: ignore
                offset=-extrusionData[name]['height']*1/4, # type: ignore
                draft=draft,
                label="width"
            )
        height =  ExtensionLine(
                border=((extrusionData[name]['width']/2, -extrusionData[name]['height']/2),(extrusionData[name]['width']/2, extrusionData[name]['height']/2)), # type: ignore
                offset=extrusionData[name]['width']*1/4, # type: ignore
                draft=draft,
                label="height"
            )
        
        newFace = extrusion_face + width + height # type: ignore
        return newFace # type: ignore


    @staticmethod
    def getExtrusionData() -> dict[str, dict[str, float | str]]: # type: ignore
        extrusionData:dict[str, dict[str, float | str]] = {}
        
        with importlib.resources.files(bd_warehouse).joinpath("data/aluminum_extrusions_I_type.csv").open("r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip the header row
            for row in reader:
                if len(row) == 0:  # skip blank rows
                    continue
                name, width, height, corner_radius, hole_dia, flange_thickness, flange_opening, flange_bottom_width, flange_max_width, flange_offset, flange_depth, flange_bottom_radius, flange_neck_top_radius, flange_neck_bottom_radius, flange_top_radius, flange_notch_width,flange_notch_depth, source = row

                extrusionData[name] = {}
                extrusionData[name]['width'] = float(width)
                extrusionData[name]['height'] = float(height)
                extrusionData[name]['corner_radius'] = float(corner_radius)
                extrusionData[name]['hole_dia'] = float(hole_dia)
                extrusionData[name]['flange_thickness'] = float(flange_thickness)
                extrusionData[name]['flange_opening'] = float(flange_opening)
                extrusionData[name]['flange_bottom_width'] = float(flange_bottom_width)
                extrusionData[name]['flange_max_width'] = float(flange_max_width)
                extrusionData[name]['flange_offset'] = float(flange_offset)
                extrusionData[name]['flange_depth'] = float(flange_depth)
                extrusionData[name]['flange_bottom_radius'] = float(flange_bottom_radius)
                extrusionData[name]['flange_neck_top_radius'] = float(flange_neck_top_radius)
                extrusionData[name]['flange_neck_bottom_radius'] = float(flange_neck_bottom_radius)
                extrusionData[name]['flange_top_radius'] = float(flange_top_radius)
                extrusionData[name]['flange_notch_width'] = float(flange_notch_width)
                extrusionData[name]['flange_notch_depth'] = float(flange_notch_depth)
                extrusionData[name]['source'] = source
        return extrusionData




if __name__ == "__main__":
    from ocp_vscode import show_all # type: ignore

    #a = AluminiumExtrusionIType(extrusion_type='Misumi HFS5-2020', length=50.0)
    #b = AluminiumExtrusionIType(extrusion_type='Item24 Profile 5 20x20', length=50.0)
    name='Misumi HFS5-2020'
    face = AluminiumExtrusionIType.getDimensionedExtrusionFace(name) # type: ignore



    show_all()