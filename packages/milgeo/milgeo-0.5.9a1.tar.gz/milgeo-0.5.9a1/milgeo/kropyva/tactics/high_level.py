import abc
from dataclasses import dataclass
import datetime
import re
from typing import Sequence

from lxml.objectify import ObjectifiedElement as KMLElement

import milgeo.kropyva.tactics.low_level as low_level
from milgeo.utils.sidc_utlis import SidcAmplifier
from milgeo.utils.svg_utils import calc_lat_lon_box, join_paths, svg_path_to_wgs, to_svg_path


URL_PATTERN = re.compile(r'url\((.*)\)', re.IGNORECASE)


def _parse_kml_time(time: str | None) -> datetime.datetime | None:
    if time is None:
        return None
    try:
        return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None

    
def _datetime_to_kml_time(dt: datetime.datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

def _get_echelon_from_kropyva_name(name: str) -> SidcAmplifier | None:
    match name:
        case 'Екіпаж': return SidcAmplifier.TEAM_CREW
        case 'Відділення': return SidcAmplifier.SQUAD
        case 'Секція': return SidcAmplifier.SECTION
        case 'Взвод': return SidcAmplifier.PLATOON_DETACHMENT
        case 'Рота': return SidcAmplifier.COMPANY_BATTERY_TROOP
        case 'Батальйон': return SidcAmplifier.BATTALION_SQUADRON
        case 'Полк': return SidcAmplifier.REGIMENT_GROUP
        case 'Бригада': return SidcAmplifier.BRIGADE
        case 'Дивізія': return SidcAmplifier.DIVISION
        case 'Корпус': return SidcAmplifier.CORPS
        case _: return None # TODO: do something with tactical groups

@dataclass
class AbstractPlacemark(abc.ABC):
    @abc.abstractmethod
    def get_type(self) -> str | None:
        '''Returns the type of the placemark. Used for the `cls` attribute in the KML'''
        pass

    @abc.abstractmethod
    def get_items(self) -> list[low_level.PlacemarkSVGItem]:
        '''Returns a list of items that define the placemark in the order they should be rendered'''
        pass

    @abc.abstractmethod
    def get_points(self) -> list[low_level.WGSCoords]:
        '''Returns a list of points that define the placemark. Used for bounding box calculation'''
        pass

    @abc.abstractmethod
    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        '''Returns the bounding box of the placemark. Returns `None` if no box is needed'''
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_color(self) -> str | None:
        pass

    @abc.abstractmethod
    def get_fill(self) -> str | None:
        pass

    @abc.abstractmethod
    def get_stroke_pattern(self) -> str | None:
        pass

    @abc.abstractmethod
    def get_creation_time(self) -> datetime.datetime | None:
        pass

    @abc.abstractmethod
    def to_low_level(self) -> low_level.RawPlacemark:
        pass

    def to_kml(self) -> KMLElement:
        """Convert to KML element by first converting to raw placemark."""
        raw_placemark = self.to_low_level()
        return raw_placemark.to_kml()


@dataclass
class BasePlacemark(AbstractPlacemark):
    name: str
    placemark_id: str = ''
    color: str | None = None
    description: str = ''
    stroke_pattern: str | None = None
    fill: str | None = None
    cls: str | None = None
    fill_opacity: float | None = None
    creation_time: datetime.datetime | None = None

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_type(self):
        '''Returns the type of the placemark. Used for the `cls` attribute in the KML'''
        return self.cls
    
    def get_color(self) -> str | None:
        return self.color

    def get_fill(self) -> str | None:
        return self.fill

    def get_stroke_pattern(self) -> str | None:
        return self.stroke_pattern

    def get_creation_time(self) -> datetime.datetime | None:
        return self.creation_time

    def to_low_level(self) -> low_level.RawPlacemark:
        # todo: defs
        midpoint = low_level.midpoint2d(self.get_points())
        midpoint = low_level.WGSCoords(x=round(midpoint.x, 6), y=round(midpoint.y, 6))
        return low_level.RawTacticPlacemark(
            name=self.get_name(),
            placemark_id=self.placemark_id,
            description=self.get_description(),
            coords=midpoint,
            items=self.get_items(),
            lat_lon_box=self.get_lat_lon_box(),
            root_svg_attrs=low_level.remove_none_values({
                'cls': self.get_type(),
                'stroke': self.get_color(),
                'fill': self.get_fill(),
                'stroke-pattern': self.get_stroke_pattern(),
                'fill-opacity': self.fill_opacity,
                'time': _datetime_to_kml_time(self.get_creation_time()),
            }),
        )


@dataclass(kw_only=True)
class Point(BasePlacemark):
    coords: low_level.WGSCoords
    url: str
    labels: list[low_level.KMLText]
    underlying_icons: Sequence[low_level.KMLIcon] = ()
    size: float = 30

    def get_points(self):
        return [self.coords]
    
    def get_items(self):
        return [
            *self.underlying_icons,
            low_level.KMLIcon(href=self.url, width=self.size, height=self.size),
            *self.labels,
        ]
    
    def get_type(self):
        match = URL_PATTERN.match(self.url)
        if match:
            return match.group(1)
        return self.url
    
    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        return None


@dataclass(kw_only=True)
class LineString(BasePlacemark): #todo: echelon
    coords: list[low_level.WGSCoords]
    labels: list[low_level.KMLText]
    echelon: SidcAmplifier | None = None

    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        return calc_lat_lon_box(self.coords)

    def get_points(self):
        return self.coords

    def get_items(self):
        return [
            low_level.KMLPath(
                points=[low_level.PathPointInfo(type={'editable', 'custom'}, index=i) for i in range(len(self.coords))],
                definition=to_svg_path(self.coords, self.get_lat_lon_box()),
            ),
            *self.labels,
        ]


@dataclass(kw_only=True)
class Polygon(BasePlacemark):
    coords: list[low_level.WGSCoords]
    labels: list[low_level.KMLText]
    echelon: SidcAmplifier | None = None

    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        return calc_lat_lon_box(self.coords)

    def get_points(self):
        return self.coords
    
    def get_items(self):
        return [
            low_level.KMLPath(
                points=[low_level.PathPointInfo(type={'editable', 'custom'}, index=i) for i in range(len(self.coords))],
                definition=to_svg_path(self.coords, self.get_lat_lon_box(), closed=True),
            ),
            *self.labels,
        ]


@dataclass(kw_only=True)
class TextObject(BasePlacemark):
    coords: low_level.WGSCoords
    label: low_level.KMLText

    def __post_init__(self):
        if not self.cls:
            self.cls = 'Текст'
        if not self.color:
            self.color = self.label.color
        if not self.fill:
            self.fill = self.label.bg

    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        return None
    
    def get_points(self):
        return [self.coords]
    
    def get_items(self):
        return [self.label]


@dataclass(kw_only=True)
class UnknownPlacemark(AbstractPlacemark):
    raw_placemark: low_level.RawPlacemark

    def get_name(self) -> str:
        return self.raw_placemark.name

    def get_description(self) -> str:
        return self.raw_placemark.description
    
    def get_color(self) -> str | None:
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.root_svg_attrs.get('stroke')
        return None

    def get_fill(self) -> str | None:
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.root_svg_attrs.get('fill')
        return None

    def get_stroke_pattern(self) -> str | None:
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.root_svg_attrs.get('stroke-pattern')
        return None
    
    def get_items(self):
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.items
        return []

    def get_lat_lon_box(self) -> low_level.LatLonBox | None:
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.lat_lon_box
        return None

    def get_points(self):
        raise NotImplementedError("Todo: implement")

    def get_type(self):
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return self.raw_placemark.root_svg_attrs.get('cls')
        return None

    def get_creation_time(self) -> datetime.datetime | None:
        if isinstance(self.raw_placemark, low_level.RawTacticPlacemark):
            return _parse_kml_time(self.raw_placemark.root_svg_attrs.get('time'))
        return None

    def to_low_level(self) -> low_level.RawPlacemark:
        return self.raw_placemark
    
    def is_tactic(self) -> bool:
        return isinstance(self.raw_placemark, low_level.RawTacticPlacemark)


class PlacemarkInferenceStrategy(abc.ABC):
    """Base class for strategies that infer high-level placemark types from low-level ones."""
    
    @abc.abstractmethod
    def infer_placemark(self, raw_placemark: low_level.RawPlacemark, **kwargs) -> AbstractPlacemark | None:
        """Try to infer a high-level placemark from a low-level one.
        
        Returns:
            A high-level placemark if inference was successful, None otherwise.
        """
        pass


class DefaultInferenceStrategy(PlacemarkInferenceStrategy):
    """Default strategy that tries to infer placemarks based on common patterns."""
    
    def infer_placemark(self, raw: low_level.RawPlacemark, curve_subpoints_count: int = 5, **kwargs) -> AbstractPlacemark | None:
        if not isinstance(raw, low_level.RawTacticPlacemark):
            return UnknownPlacemark(raw_placemark=raw)
        
        icons = [item for item in raw.items if isinstance(item, low_level.KMLIcon)]
        paths = [item for item in raw.items if isinstance(item, low_level.KMLPath)]
        texts = [item for item in raw.items if isinstance(item, low_level.KMLText)]
        
        fill_opacity_str = raw.root_svg_attrs.get('fill-opacity')
        fill_opacity = float(fill_opacity_str) if fill_opacity_str else None

        # Point: has an icon but no paths
        if icons and not paths:
            return Point(
                name=raw.name,
                description=raw.description,
                coords=raw.coords or low_level.WGSCoords(x=0, y=0),
                url=icons[-1].href,  # Use last icon as main
                labels=texts,
                underlying_icons=icons[:-1],  # Rest of icons as underlying
                size=icons[-1].width,  # Use last icon's size
                color=raw.root_svg_attrs.get('stroke'),
                fill=raw.root_svg_attrs.get('fill'),
                stroke_pattern=raw.root_svg_attrs.get('stroke-pattern'),
                cls=raw.root_svg_attrs.get('cls'),
                fill_opacity=fill_opacity,
                creation_time=_parse_kml_time(raw.root_svg_attrs.get('time')),
            )
        
        # LineString or Polygon: has a path with points
        elif len(paths) > 0 and raw.lat_lon_box is not None:
            path = join_paths(p.definition for p in paths)
            coords, is_closed = svg_path_to_wgs(path, raw.lat_lon_box, curve_subpoints=curve_subpoints_count)
            if not coords:
                return None
            
            echelon = None
            for path in paths:
                if echelon := self._get_echelon(path):
                    break
            
            def _get_path_attr(attr: str):
                '''Get attribute from any path (or root svg attrs as fallback)'''
                return next((item.other_attributes.get(attr)
                             for item in paths
                             if item.other_attributes.get(attr)),
                             raw.root_svg_attrs.get(attr))
            
            if not is_closed:
                return LineString(
                    name=raw.name,
                    description=raw.description,
                    coords=coords,
                    labels=texts,
                    echelon=echelon,
                    color=_get_path_attr('stroke'),
                    fill=_get_path_attr('fill'),
                    stroke_pattern=_get_path_attr('stroke-pattern'),
                    cls=raw.root_svg_attrs.get('cls'),
                    fill_opacity=fill_opacity,
                    creation_time=_parse_kml_time(raw.root_svg_attrs.get('time')),
                )
            else:
                return Polygon(
                    name=raw.name,
                    description=raw.description,
                    coords=coords,
                    labels=texts,
                    echelon=echelon,
                    color=_get_path_attr('stroke'),
                    fill=_get_path_attr('fill'),
                    stroke_pattern=_get_path_attr('stroke-pattern'),
                    fill_opacity=fill_opacity,
                    cls=raw.root_svg_attrs.get('cls'),
                    creation_time=_parse_kml_time(raw.root_svg_attrs.get('time')),
                )
        
        # TextObject: has a text and no icons or paths
        elif texts and not icons and not paths:
            return TextObject(
                name=raw.name,
                description=raw.description,
                coords=raw.coords or low_level.WGSCoords(x=0, y=0),
                label=texts[0],
                cls=raw.root_svg_attrs.get('cls'),
                color=raw.root_svg_attrs.get('stroke'),
                fill=raw.root_svg_attrs.get('fill'),
                stroke_pattern=raw.root_svg_attrs.get('stroke-pattern'),
                fill_opacity=fill_opacity,
                creation_time=_parse_kml_time(raw.root_svg_attrs.get('time')),
            )
        
        return None
    
    def _get_echelon(self, kml_path: low_level.KMLPath) -> SidcAmplifier | None:
        markers = [
            kml_path.other_attributes.get('marker-start'),
            kml_path.other_attributes.get('marker-end'),
            *(p.marker for p in kml_path.points)
        ]
        for marker in markers:
            if not marker:
                continue
            if echelon := self._get_echelon_from_marker(marker):
                return echelon
        return None
        
    def _get_echelon_from_marker(self, marker_url: str) -> SidcAmplifier | None:
        match = URL_PATTERN.match(marker_url)
        url = match.group(1) if match else marker_url
        return _get_echelon_from_kropyva_name(url)


@dataclass
class Folder:
    """High-level representation of a KML folder."""
    name: str
    placemarks: list[AbstractPlacemark]
    subfolders: list['Folder']
    
    def to_low_level(self) -> low_level.RawFolder:
        """Convert back to a raw folder."""
        return low_level.RawFolder(
            name=self.name,
            placemarks=[p.to_low_level() for p in self.placemarks],
            subfolders=[f.to_low_level() for f in self.subfolders]
        )
    
    def to_kml(self) -> KMLElement:
        """Convert directly to KML."""
        return self.to_low_level().to_kml()
    
    def nested_placemarks(self):
        """Iterate over all nested placemarks in the folder and its subfolders."""
        for placemark in self.placemarks:
            yield placemark
        for subfolder in self.subfolders:
            yield from subfolder.nested_placemarks()


class KMLParser:
    """Parser for converting KML/KME files into high-level placemark and folder structures."""
    
    def __init__(self,
                 strategies: list[PlacemarkInferenceStrategy] | None = None,
                 raw_parser: low_level.RawKMLParser = low_level.RawKMLParser(),
                 curve_subpoints_count: int = 5):
        """Initialize with inference strategies and a raw parser.
        
        Args:
            strategies: List of strategies to try in order. If None, uses DefaultInferenceStrategy.
            raw_parser: Parser for raw KML structures. If None, uses default RawKMLParser.
            curve_subpoints_count: Number of subpoints to use for curve interpolation.
        """
        self.strategies = strategies or [DefaultInferenceStrategy()]
        self.raw_parser = raw_parser
        self.curve_subpoints_count = curve_subpoints_count
    
    def parse_placemark(self, kml: low_level.RawPlacemark | KMLElement | str | bytes) -> AbstractPlacemark:
        """Parse a KML placemark into a high-level placemark.
        
        Args:
            kml: KML content as an element, string, or bytes
            
        Returns:
            High-level placemark. Falls back to UnknownPlacemark if no strategy works.
        """
        if isinstance(kml, low_level.RawPlacemark):
            raw_placemark = kml
        elif isinstance(kml, KMLElement) or isinstance(kml, str) or isinstance(kml, bytes):
            raw_placemark = self.raw_parser.parse_placemark(kml)
        else:
            raise ValueError(f"Invalid type for kml: {type(kml)}")
        
        for strategy in self.strategies:
            result = strategy.infer_placemark(raw_placemark, curve_subpoints_count=self.curve_subpoints_count)
            if result is not None:
                return result
        
        # If no strategy worked, return as unknown
        return UnknownPlacemark(raw_placemark=raw_placemark)
    
    def parse_folder(self, folder: low_level.RawFolder) -> Folder:
        """Parse a raw folder into a high-level one."""
        return Folder(
            name=folder.name,
            placemarks=[self.parse_placemark(p) for p in folder.placemarks],
            subfolders=[self.parse_folder(f) for f in folder.subfolders]
        )

    def parse_document(self, kml: KMLElement | str | bytes) -> Folder:
        """Parse a KML document into a high-level folder structure.
        
        Args:
            kml: KML content as an element, string, or bytes
            
        Returns:
            High-level folder structure containing parsed placemarks.
        """
        raw_folder = self.raw_parser.parse_document(kml)
        return self.parse_folder(raw_folder)


def parse_document(kml: KMLElement | str | bytes, strategies: list[PlacemarkInferenceStrategy] | None = None) -> Folder:
    """Parse a KML document into a high-level folder structure.
    
    Args:
        kml: KML content as an element, string, or bytes
        strategies: Optional list of inference strategies to use
        
    Returns:
        High-level folder structure containing parsed placemarks.
    """
    parser = KMLParser(strategies=strategies)
    return parser.parse_document(kml)

def parse_placemark(kml: KMLElement | str | bytes, strategies: list[PlacemarkInferenceStrategy] | None = None) -> AbstractPlacemark:
    """Parse a KML placemark into a high-level placemark.
    
    Args:
        kml: KML content as an element, string, or bytes
        strategies: Optional list of inference strategies to use
        
    Returns:
        High-level placemark. Falls back to UnknownPlacemark if no strategy works.
    """
    parser = KMLParser(strategies=strategies)
    return parser.parse_placemark(kml)
