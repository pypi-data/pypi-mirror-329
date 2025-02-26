import abc
from dataclasses import dataclass, field
from typing import Literal, Sequence

from lxml.objectify import fromstring
from lxml.objectify import ObjectifiedElement as KMLElement
from pykml.factory import KML_ElementMaker as KML
import svgpathtools as svg

from milgeo.utils.coords import WGSCoords, _TCoordPair
from milgeo.utils.svg_utils import LatLonBox, round_path_points
from milgeo.utils.kml_utils import deepgetattr, strip_tag_namespace


def remove_none_values(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}

def lat_lon_box_to_kml(bbox: LatLonBox) -> KMLElement:
    return KML.Region(KML.LatLonAltBox(
        KML.west(bbox.west),
        KML.east(bbox.east),
        KML.north(bbox.north),
        KML.south(bbox.south),
    ))


class PlacemarkSVGItem(abc.ABC):
    @abc.abstractmethod
    def to_kml(self) -> KMLElement:
        pass


_TextAnchor = Literal['start', 'middle', 'end']


@dataclass(kw_only=True)
class KMLText(PlacemarkSVGItem):
    text: str
    x: float | None = None
    y: float | None = None
    dx: float | None = None
    dy: float | None = None

    color: str | None = 'black'
    bg: str | None = None
    font_family: str = 'Arial'
    font_size: float = 13
    text_anchor: _TextAnchor = 'middle'
    font_weight: str | None = "bold"
    alignment_baseline: str = 'text-before-edge'
    anchor_style: str = 'none'
    other_attributes: dict[str, str] = field(default_factory=dict)
    fill_opacity: float | None = None

    def to_kml(self) -> KMLElement:
        attributes = {
            'fill': self.color,
            'bg': self.bg,
            'font-family': self.font_family,
            'font-size': self.font_size,
            'font-weight': self.font_weight,
            'text-anchor': self.text_anchor,
            'anchor-style': self.anchor_style,
            'alignment-baseline': self.alignment_baseline,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'fill-opacity': self.fill_opacity,
            **self.other_attributes,
        }
        return KML.text(self.text, **{k: str(v) for k, v in attributes.items() if v is not None})


@dataclass
class KMLIcon(PlacemarkSVGItem):
    href: str
    width: float
    height: float
    stroke_width: float = 2
    other_attributes: dict[str, str] = field(default_factory=dict)

    def to_kml(self) -> KMLElement:
        return KML.use(
            href=self.href,
            width=str(self.width),
            height=str(self.height),
            **{
                'stroke-width': str(self.stroke_width),
            },
            **self.other_attributes,
        )


@dataclass
class PathPointInfo:
    type: set[str]
    marker: str | None = None
    index: int | None = None
    other_attributes: dict[str, str] = field(default_factory=dict)

    def to_kml(self, index=None) -> KMLElement:
        attributes = {
            'index': index if index is not None else self.index,
            'type': ' '.join(sorted(self.type)),
            'marker': self.marker,
            **self.other_attributes,
        }
        return KML.point(**{k: str(v) for k, v in attributes.items() if v is not None})
    

@dataclass
class KMLPath(PlacemarkSVGItem):
    points: list[PathPointInfo]
    definition: svg.Path
    stroke_width: float = 2
    other_attributes: dict[str, str] = field(default_factory=dict)

    def to_kml(self) -> KMLElement:
        return KML.path(*(p.to_kml(index=i) for i, p in enumerate(self.points)),
                        **{
                            'd': self.definition.d(use_closed_attrib=True),
                            'stroke-width': str(self.stroke_width),
                        },
                        **self.other_attributes,
                        )


@dataclass
class KMLUnknownItem(PlacemarkSVGItem):
    raw_kml: KMLElement

    def to_kml(self) -> KMLElement:
        return self.raw_kml


def midpoint2d(points: Sequence[_TCoordPair]) -> _TCoordPair:
    sum_x = sum(p.x for p in points)
    sum_y = sum(p.y for p in points)
    n = len(points)
    return type(points[0])(x=sum_x / n, y=sum_y / n)


@dataclass(kw_only=True)
class RawPlacemark(abc.ABC):
    name: str
    description: str = ''

    @abc.abstractmethod
    def to_kml(self) -> KMLElement:
        pass

@dataclass(kw_only=True)
class RawUnknownPlacemark(RawPlacemark):
    raw_kml: KMLElement

    def to_kml(self) -> KMLElement:
        return self.raw_kml

@dataclass(kw_only=True)
class RawTacticPlacemark(RawPlacemark):
    placemark_id: str = ""
    coords: WGSCoords | None = None

    '''Items of `ExtendedData.svg.g` element.'''
    items: list[PlacemarkSVGItem]
    lat_lon_box: LatLonBox | None

    '''Attributes of the root SVG group (ExtendedData.svg.g).'''
    root_svg_attrs: dict[str, str] = field(default_factory=dict)

    def to_kml(self) -> KMLElement:
        x, y = self.coords.xy if self.coords is not None else (0, 0)
        x = round(x, 6)
        y = round(y, 6)
        kml = KML.Placemark(
            KML.name(self.name),
            KML.description(self.description or ''),
            KML.Point(KML.coordinates(f'{x},{y}')),
            KML.ExtendedData(KML.svg(KML.g(
                *(item.to_kml() for item in self.items),
                **self.root_svg_attrs,
            )))
        )
        if self.lat_lon_box is not None:
            kml.append(lat_lon_box_to_kml(self.lat_lon_box))
        if self.placemark_id:
            kml.set('id', self.placemark_id)
        return kml


@dataclass(kw_only=True)
class RawFolder:
    name: str
    folder_id: str = ""
    placemarks: list[RawPlacemark] = field(default_factory=list)
    subfolders: list['RawFolder'] = field(default_factory=list)

    def to_kml(self) -> KMLElement:
        folder = KML.Folder(
            KML.name(self.name),
            *(subfolder.to_kml() for subfolder in self.subfolders),
            *(placemark.to_kml() for placemark in self.placemarks),
        )
        if self.folder_id:
            folder.set('id', self.folder_id)
        return folder
    
    def to_kml_document(self) -> KMLElement:
        document = KML.Document(
            KML.open(1),
            KML.name(self.name),
            *(subfolder.to_kml() for subfolder in self.subfolders),
            *(placemark.to_kml() for placemark in self.placemarks),
        )
        if self.folder_id:
            document.set('id', self.folder_id)
        return KML.kml(document)

class RawKMLParser:
    """Parser for KML/KME files that creates raw placemark and folder structures."""
    
    def __init__(self, svg_parser=None):
        self.svg_parser = svg_parser or self.default_svg_parser
    
    def parse_placemark(self, kml: KMLElement | str | bytes) -> RawPlacemark:
        """Parse a KML Placemark element into a RawPlacemark object."""
        if isinstance(kml, str):
            kml_element = fromstring(kml)
        elif isinstance(kml, bytes):
            kml_element = fromstring(kml.decode('utf-8')) # assume utf-8 encoding when parsing a single placemark
        elif isinstance(kml, KMLElement):
            kml_element = kml
        else:
            raise ValueError(f"Invalid type for kml: {type(kml)}")
        
        tag = strip_tag_namespace(kml_element)
        if tag != 'Placemark':
            raise ValueError(f"Expected Placemark tag, but got '{tag}'")

        placemark_id = kml_element.get('id')
        name = deepgetattr(kml_element, 'name.text', '') or ''
        description = deepgetattr(kml_element, 'description.text', '') or ''
        
        svg_group = deepgetattr(kml_element, 'ExtendedData.svg.g')
        if svg_group is None:
            return RawUnknownPlacemark(name=name, description=description, raw_kml=kml_element)
        
        coords = None
        if (coords_str := deepgetattr(kml_element, 'Point.coordinates.text')) is not None and coords_str:
            coord_parts = coords_str.strip().split(',')
            coords = WGSCoords(y=float(coord_parts[1]), x=float(coord_parts[0]))
        
        lat_lon_box = None
        if (box := deepgetattr(kml_element, 'Region.LatLonAltBox')) is not None:
            lat_lon_box = LatLonBox(
                north=float(box.north), # type: ignore
                south=float(box.south), # type: ignore
                east=float(box.east), # type: ignore
                west=float(box.west) # type: ignore
            )
        
        root_svg_attrs = {str(k): str(v) for k, v in svg_group.attrib.items()}
        items = self.svg_parser(svg_group)
        
        return RawTacticPlacemark(
            placemark_id=placemark_id or '',
            name=name,
            description=description,
            coords=coords,
            items=items,
            lat_lon_box=lat_lon_box,
            root_svg_attrs=root_svg_attrs,
        )
    
    def parse_folder(self, folder_element: KMLElement) -> RawFolder:
        """Parse a KML Folder or Document element into a RawFolder."""
        folder_id = folder_element.get('id')
        name = deepgetattr(folder_element, 'name.text', '')
        placemarks = []
        subfolders = []
        
        for element in folder_element.iterchildren():
            assert isinstance(element, KMLElement), f"Expected element of type KMLElement, but got {type(element)}"
            tag = strip_tag_namespace(element)
            
            if tag == 'Folder':
                subfolders.append(self.parse_folder(element))
            elif tag == 'Placemark':
                placemarks.append(self.parse_placemark(element))
            else:
                # Skip other elements like name, description, etc.
                print(f"Unknown tag in folder: '{tag}'")
        
        return RawFolder(
            folder_id=folder_id or '',
            name=name,
            placemarks=placemarks,
            subfolders=subfolders
        )
    
    def parse_document(self, kml: KMLElement | str | bytes) -> RawFolder:
        """Parse a KML document into a RawFolder structure."""
        if isinstance(kml, str):
            kml_element = fromstring(kml)
        elif isinstance(kml, bytes):
            kml_element = fromstring(kml)
        elif isinstance(kml, KMLElement):
            kml_element = kml
        else:
            raise ValueError(f"Invalid type for kml: {type(kml)}")
        
        # Handle both Document and Folder elements
        if strip_tag_namespace(kml_element) == 'kml':
            if hasattr(kml_element, 'Document'):
                return self.parse_folder(kml_element.Document)
            else:
                raise ValueError("KML element must contain a Document")
        else:
            return self.parse_folder(kml_element)
    
    @staticmethod
    def default_svg_parser(svg_group: KMLElement) -> list[PlacemarkSVGItem]:
        """Default parser for SVG elements within a placemark."""
        items = []
        kml_ns = svg_group.nsmap[None]
        
        for element in svg_group.iterchildren():
            tag = strip_tag_namespace(element)
            
            if tag == 'text':
                x = element.get('x')
                y = element.get('y')
                dx = element.get('dx')
                dy = element.get('dy')
                items.append(KMLText(
                    text=element.text or '',
                    x=float(x) if x is not None else None,
                    y=float(y) if y is not None else None,
                    dx=float(dx) if dx is not None else None,
                    dy=float(dy) if dy is not None else None,
                    color=element.get('fill'),
                    bg=element.get('bg'),
                    font_family=element.get('font-family', 'Arial'),
                    font_size=int(element.get('font-size', 13)),
                    text_anchor=element.get('text-anchor', 'middle'), # type: ignore
                    font_weight=element.get('font-weight'),
                    alignment_baseline=element.get('alignment-baseline', 'text-before-edge'),
                    anchor_style=element.get('anchor-style', 'none'),
                    other_attributes={str(k): str(v) for k, v in element.attrib.items() 
                                   if k not in {'x', 'y', 'dx', 'dy', 'fill', 'bg', 'font-family',
                                              'font-size', 'text-anchor', 'font-weight',
                                              'alignment-baseline', 'anchor-style'}}
                ))
            
            elif tag == 'use':
                items.append(KMLIcon(
                    href=element.get('href', ''),
                    width=float(element.get('width', 0)),
                    height=float(element.get('height', 0)),
                    stroke_width=float(element.get('stroke-width', 2)),
                    other_attributes={str(k): str(v) for k, v in element.attrib.items()
                                   if k not in {'href', 'width', 'height', 'stroke-width'}}
                ))
            
            elif tag == 'path':
                # Parse path points
                points = []
                for point in element.iterchildren(tag=f'{{{kml_ns}}}point'):
                    point_type = set(point.get('type', '').split())
                    index = point.get('index')
                    points.append(PathPointInfo(
                        type=point_type,
                        marker=point.get('marker'),
                        index=int(index) if index is not None else None,
                        other_attributes={str(k): str(v) for k, v in point.attrib.items()
                                       if k not in {'type', 'marker', 'index'}}
                    ))
                
                # Parse path definition
                path_def = round_path_points(svg.parse_path(element.get('d', '')), 5)
                items.append(KMLPath(
                    points=points,
                    definition=path_def,
                    stroke_width=float(element.get('stroke-width', 2)),
                    other_attributes={str(k): str(v) for k, v in element.attrib.items()
                                   if k not in {'d', 'stroke-width'}}
                ))
            
            else:
                items.append(KMLUnknownItem(raw_kml=element)) # type: ignore
        
        return items


# Convenience functions
def parse_kml_document(kml: KMLElement | str | bytes) -> RawFolder:
    parser = RawKMLParser()
    return parser.parse_document(kml)

def parse_placemark(kml: KMLElement | str | bytes) -> RawPlacemark:
    parser = RawKMLParser()
    return parser.parse_placemark(kml)
