import io
import zipfile
from typing import Type, Union

import html2text
from lxml.objectify import ObjectifiedElement as KMLElement

from milgeo import GeometriesList, Point, Line, Polygon
from milgeo.config import Config
from milgeo.extractor import ExtractionError, ExtractorContext, GeometryExtractor, InvalidPasswordError, PasswordRequiredError
from milgeo.geometry import Geometry
from milgeo.kropyva.tactics import high_level, low_level
from milgeo.kropyva.url_mapping import UrlToSidcMapping
from milgeo.utils.datetime_utils import format_observation_datetime
from milgeo.utils.kme_utils import is_kme_file, read_kme, InvalidPasswordException
from milgeo.color import ColorFinder
from milgeo.utils.sidc_utlis import get_sidc_identity_from_color, set_sidc_amplifier, set_sidc_identity


DELTA_TEXT_SIDC = "10016600009100000000"

class TacticsExtractor(GeometryExtractor):
    """
    Extracts geometries from Kropyva Tactics files
    Uses embedded_kml_extractor to extract embedded non-Kropyva (Google, AlpineQuest, etc.) KML placemarks from KME files
    Uses high_level.KMLParser to parse the files
    Uses UrlToSidcMapping to map Kropyva URLs to SIDC codes
    Uses ColorFinder to find the color of the geometry

    """
    def __init__(self,
                 embedded_kml_extractor: GeometryExtractor | None = None,
                 parser: high_level.KMLParser | None = None,
                 url_mapping: UrlToSidcMapping | None = None,
                 color_finder: ColorFinder | None = None,
                 curve_subpoints_count: int = 5,
                 outline_color_from_placemark: bool = True):
        self.embedded_kml_extractor = embedded_kml_extractor
        self.parser = parser or high_level.KMLParser(curve_subpoints_count=curve_subpoints_count)
        self.url_to_sidc_mapping = url_mapping or UrlToSidcMapping()
        self.color_finder = color_finder or ColorFinder()
        self.html_to_text = html2text.HTML2Text()
        self.html_to_text.ignore_images = True
        self.html_to_text.ignore_emphasis = True
        self.html_to_text.ignore_links = True
        self.html_to_text.ignore_tables = True

        self.curve_subpoints_count = curve_subpoints_count
        self.outline_color_from_placemark = outline_color_from_placemark
    
    def extract_file(self, file, context: ExtractorContext | None = None) -> GeometriesList:
        try:
            if is_kme_file(file):
                if context is None or context.password is None:
                    raise PasswordRequiredError("Password is required for KME files")
                return self._extract_from_kme(file, password=context.password)
            elif zipfile.is_zipfile(file):
                return self._extract_from_kmz(file)
            else:
                return self._extract_from_kml(file)
        except InvalidPasswordException as e:
            raise InvalidPasswordError("Invalid KME password") from e
        except PasswordRequiredError as e:
            raise
        except Exception as e:
            raise ExtractionError("Error extracting geometries from file") from e

    def _extract_from_kme(self, file, password: str):
        kme_content = read_kme(password, file)
        return self._extract_from_kmz(io.BytesIO(kme_content))

    def _extract_from_kmz(self, file):
        with zipfile.ZipFile(file, 'r') as kmz:
            for name in kmz.namelist():
                if name.endswith('.kml'):
                    with kmz.open(name) as kml_file:
                        return self._extract_from_kml(kml_file)
        return GeometriesList()

    def _extract_from_kml(self, kml_file):
        kml_file.seek(0)
        tree = self.parser.parse_document(kml_file.read())
        geometries = GeometriesList()
        for placemark in tree.nested_placemarks():
            geometry = self._process_geometry(placemark)
            if geometry:
                geometries.add_geometry(geometry)
        return geometries

    def extract_object(self, obj: KMLElement, context: ExtractorContext | None = None) -> Geometry | None:
        placemark = self.parser.parse_placemark(obj)
        return self._process_geometry(placemark)

    def requires_password(self, file) -> bool:
        return is_kme_file(file)

    def _process_geometry(self, placemark: high_level.AbstractPlacemark):
        if isinstance(placemark, high_level.UnknownPlacemark) and isinstance(placemark.raw_placemark, low_level.RawUnknownPlacemark):
            if self.embedded_kml_extractor:
                return self.embedded_kml_extractor.extract_object(placemark.raw_placemark.raw_kml)
            return

        metadata = {}

        name = placemark.get_name() or ""
        if isinstance(placemark, high_level.TextObject): # TODO: this is a hack because delta doesn't support importing text objects as GEOJSON
            label_text = self.html_to_text.handle(placemark.label.text or '').strip()
            metadata['name'] = name
            metadata['text'] = label_text
            metadata['text_font_size'] = placemark.label.font_size
            metadata['text_font_color'] = self.color_finder.find_hex_color(placemark.label.color)
            metadata['text_background_color'] = self.color_finder.find_hex_color(placemark.label.bg)
            name = label_text or placemark.get_name() or ''
            
        description = placemark.get_description() or ""
        stroke_color = placemark.get_color()
        
        sidc = self._determine_sidc(placemark)

        geometry_type = self._determine_geometry_type(placemark)
        if not geometry_type:
            return
    
        coordinates = self._get_coordinates(placemark)
        if not coordinates:
            return

        try:
            creation_time = placemark.get_creation_time()
            observation_datetime = format_observation_datetime(creation_time) if creation_time else None
            return self._create_geometry(
                geometry_type=geometry_type,
                name=name,
                coordinates=coordinates,
                description=description,
                metadata={},
                observation_datetime=observation_datetime,
                sidc=sidc,
                outline_color=stroke_color if self.outline_color_from_placemark else None,
                fill_color=placemark.get_fill(),
                fill_opacity=getattr(placemark, 'fill_opacity', None)
            )
        except ValueError as e:
            print(f"Error creating geometry: {e}")

    def _get_basic_sidc(self, geometry_type: Type) -> str:
        """Get the basic SIDC code based on geometry type."""
        if geometry_type == Point:
            return "10012500001313000000"
        elif geometry_type == Line:
            return "10016600001100000000"
        elif geometry_type == Polygon:
            return "10012500001501000000"
        return "10012500001313000000"

    @staticmethod
    def _determine_geometry_type(placemark: high_level.AbstractPlacemark) -> Union[Type[Point], Type[Line], Type[Polygon], None]:
        match placemark:
            case high_level.Point():
                return Point
            case high_level.LineString():
                return Line
            case high_level.Polygon():
                return Polygon
            case high_level.TextObject():
                return Point
            case _:
                return None # TODO: try to infer

    def _should_reverse_points(self, placemark: high_level.AbstractPlacemark) -> bool:
        placemark_type = placemark.get_type()
        if not placemark_type:
            return False
        url_properties = self.url_to_sidc_mapping.find_entry(placemark_type)
        return url_properties is not None and url_properties.reverse_points

    def _get_coordinates(self, placemark: high_level.AbstractPlacemark) -> list[float] | list[list[float]] | list[list[list[float]]]:
        match placemark:
            case high_level.Point():
                return list(placemark.get_points()[0].xy)
            case high_level.LineString():
                points = [list(point.xy) for point in placemark.get_points()]
                if self._should_reverse_points(placemark):
                    points.reverse()
                return points
            case high_level.Polygon():
                outer_ring_points = [list(point.xy) for point in placemark.get_points()]
                outer_ring = [*outer_ring_points, *outer_ring_points[:1]] # close the polygon
                return [outer_ring]
            case high_level.TextObject():
                return list(placemark.coords.xy)
            case _:
                return []

    def _create_geometry(self, geometry_type: Type[Geometry], name: str, sidc: str, coordinates: list, description: str, metadata,
                         outline_color: str | None = None, fill_color: str | None = None, fill_opacity: float | None = None, observation_datetime: str | None = None):
        print(f"Creating geometry: {geometry_type.__name__}, name={name}, sidc={sidc}, coordinates={coordinates}, description={description}, metadata={metadata}, outline_color={outline_color}, fill_color={fill_color}, fill_opacity={fill_opacity}, observation_datetime={observation_datetime}")
        if fill_opacity is None:
            if geometry_type == Polygon:
                fill_opacity_str = "1.0"
            else:
                fill_opacity_str = None
        else:
            fill_opacity_str = str(fill_opacity)
        geometry = geometry_type(name=name,
                                    sidc=sidc,
                                    coordinates=coordinates,
                                    metadata=metadata,
                                    comments=[description] if description else [],
                                    observation_datetime=observation_datetime,
                                    outline_color=self.color_finder.find_hex_color(outline_color),
                                    fill_color=self.color_finder.find_hex_color(fill_color),
                                    fill_opacity=fill_opacity_str)
        # geometry.find_sidc() # TODO: compare with sidc from the icon
        return geometry
    
    def _determine_sidc(self, placemark: high_level.AbstractPlacemark) -> str:
        '''For now, just determine the SIDC from the placemark type'''

        if isinstance(placemark, high_level.TextObject):
            # return DELTA_TEXT_SIDC # TODO: this is how it should be done, but delta doesn't support importing text objects
            sidc = Config.default_sidc or self._get_basic_sidc(Point)
            sidc = set_sidc_identity(sidc, get_sidc_identity_from_color(placemark.get_color() or ''))
            return sidc

        placemark_type = placemark.get_type()
        placemark_color = placemark.get_color()
        identity_from_color = get_sidc_identity_from_color(placemark_color)
        type_based_sidc = placemark_type and self.url_to_sidc_mapping.map_url(placemark_type, identity_from_color=identity_from_color)
        if not type_based_sidc:
            basic_sidc = self._get_basic_sidc(self._determine_geometry_type(placemark) or type(None))
            type_based_sidc = set_sidc_identity(basic_sidc, identity_from_color)

        stroke_pattern = placemark.get_stroke_pattern()
        if stroke_pattern:
            modified_sidc = self.url_to_sidc_mapping.map_url(stroke_pattern, identity_from_color=None, base_sidc=type_based_sidc)
            if modified_sidc:
                return modified_sidc

        if isinstance(placemark, high_level.LineString) or isinstance(placemark, high_level.Polygon):
            if placemark.echelon:
                return set_sidc_amplifier(type_based_sidc, placemark.echelon)

        return type_based_sidc
