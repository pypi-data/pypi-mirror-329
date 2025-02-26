import csv
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List, Dict, Optional, Union
import uuid

from milgeo import FeatureBuilder, PlacemarkBuilder, CSVBuilder, NVGBuilder
from milgeo import ColorFinder
from milgeo import PlatformType, ReliabilityCredibility
from milgeo.config import Config
from lxml import etree

from milgeo.utils.kmz_utils import create_kmz_archive, save_kml_document, save_svg_as_png, add_style_to_document, add_style_url_to_placemark
from milgeo.utils.iter_utils import batched


@dataclass
class Geometry:
    name: str
    coordinates: List # X, Y
    metadata: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))

    id: Optional[str] = None
    sidc: Optional[str] = None
    observation_datetime: Optional[str] = None
    reliability_credibility: Optional[ReliabilityCredibility] = None
    staff_comments: Optional[str] = None
    platform_type: Optional[PlatformType] = None
    quantity: Optional[str] = None
    direction: Optional[str] = None
    speed: Optional[str] = None
    comments: Optional[List[str]] = field(default_factory=list)
    outline_color: Optional[str] = None
    fill_color: Optional[str] = None
    fill_opacity: Optional[str] = None

    def __post_init__(self):
        self.unit_designator = Config.get_unit_designator()

        if self.sidc is None or self.sidc == "":
            self.sidc = self.default_sidc

        if self.name is None:
            self.name = ""

        if self.sidc and len(self.sidc) != 20:
            raise ValueError("sidc must be exactly 20 digits.")
        
        if self.platform_type and not isinstance(self.platform_type, PlatformType):
            raise ValueError("platform_type must be an instance of PlatformType.")

        self.validate_coordinates()

        if isinstance(self, Point):
            if not isinstance(self.coordinates, list) or len(self.coordinates) != 2:
                raise ValueError("Point must have exactly 2 coordinate values (longitude, latitude).")
            if not all(isinstance(coord, (int, float)) for coord in self.coordinates):
                raise ValueError("Each coordinate in a Point must be a float or an integer.")

        elif isinstance(self, Line):
            if not all(isinstance(line, list) and len(line) == 2 for line in self.coordinates):
                raise ValueError("LineString must be a list of at least 2 coordinate tuples (longitude, latitude).")
            if len(self.coordinates) < 2:
                raise ValueError("LineString must have at least 2 coordinate tuples.")

        elif isinstance(self, Polygon):
            if not all(isinstance(ring, list) for ring in self.coordinates):
                raise ValueError("Polygon must be a list of LinearRings.")
            for ring in self.coordinates:
                if len(ring) < 4:
                    raise ValueError("Each LinearRing in a Polygon must have at least 4 coordinate tuples.")
                if ring[0] != ring[-1]:
                    raise ValueError("The first and last coordinate pairs in a LinearRing must be the same.")
                if not all(isinstance(coord, list) and len(coord) == 2 for coord in ring):
                    raise ValueError("Each coordinate in a LinearRing must be "
                                     "a list of 2 float values (longitude, latitude).")

        if self.reliability_credibility and not isinstance(self.reliability_credibility, ReliabilityCredibility):
            raise ValueError(
                f"reliability_credibility '{self.reliability_credibility}' is not a valid ReliabilityCredibility value.")

        hex_color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$')

        if self.outline_color and not hex_color_pattern.match(self.outline_color):
            raise ValueError(f"outline_color '{self.outline_color}' is not a valid HEX color.")

        if self.fill_color:
            if not hex_color_pattern.match(self.fill_color):
                raise ValueError(f"fill_color '{self.fill_color}' is not a valid HEX color.")
            if not self.fill_opacity or not 0 <= float(self.fill_opacity) <= 1:
                raise ValueError(
                    f"fill_opacity '{self.fill_opacity}' must be a number between 0 and 1 when fill_color is specified.")

        if self.observation_datetime:
            try:
                datetime.strptime(self.observation_datetime, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError(
                    f"observation_datetime '{self.observation_datetime}' "
                    f"is not a valid timestamp in the format yyyy-MM-ddThh:mm:ss.")

        if self.quantity:
            try:
                int_quantity = int(self.quantity)
                if str(int_quantity) != self.quantity:
                    raise ValueError()
            except ValueError:
                raise ValueError(f"quantity '{self.quantity}' must be a string representing an integer.")

    def validate_coordinates(self):
        if not self.coordinates:
            raise ValueError("coordinates cannot be empty.")
        if isinstance(self, Point):
            self._validate_point()
        elif isinstance(self, Line):
            self._validate_line()
        elif isinstance(self, Polygon):
            self._validate_polygon()

    def _validate_point(self):
        if not isinstance(self.coordinates, list) or len(self.coordinates) != 2:
            raise ValueError(f"Point must have exactly 2 coordinates, got {self.coordinates}")

        x, y = self.coordinates
        if not (-180 <= x <= 180 and -90 <= y <= 90):
            raise ValueError(f"Coordinates must be in X:[-180...180] and Y:[-90...90], but got X: {x}, Y: {y}.")

    def _validate_line(self):
        for coord in self.coordinates:
            if not isinstance(coord, list) or len(coord) != 2:
                raise ValueError(f"LineString must consist of 2-element coordinate pairs, but got {coord}")
            x, y = coord
            if not (-180 <= x <= 180 and -90 <= y <= 90):
                raise ValueError(f"Invalid coordinate in LineString: X: {x}, Y: {y}. Must be in X:[-180...180] and Y:[-90...90].")

    def _validate_polygon(self):
        for ring in self.coordinates:
            if not isinstance(ring, list):
                raise ValueError(f"Polygon must consist of LinearRings, but got {ring}")
            for coord in ring:
                if not isinstance(coord, list) or len(coord) != 2:
                    raise ValueError(f"LinearRing must consist of 2-element coordinate pairs, but got {coord}")
                x, y = coord
                if not (-180 <= x <= 180 and -90 <= y <= 90):
                    raise ValueError(f"Invalid coordinate in Polygon: X: {x}, Y: {y}. Must be in X:[-180...180] and Y:[-90...90].")

    @property
    def geometry_type(self):
        raise NotImplementedError("Subclasses should implement this property")

    @property
    def default_sidc(self):
        raise NotImplementedError("Subclasses should implement this property")

    def find_outline_color(self, string: str, finder=ColorFinder()):
        self.outline_color = finder.find_hex_color(string)

    def find_sidc(self, string: str | None = None):
        if isinstance(self, Point):
            concat_string = string or ''.join(filter(None, [
                self.name,
                ''.join(self.comments or []) if Config.sidc_from_comments else None,
                self.outline_color if Config.sidc_from_comments else None
            ]))

            if concat_string:
                matched = self.unit_designator.calculate_icon(concat_string)
                self.sidc = matched.sidc
                if not self.name:
                    self.name = matched.matched_text

    def map_enum_field(self, enum_class, string: str):
        if enum_class not in [PlatformType, ReliabilityCredibility]:
            raise ValueError("Invalid class. Only PlatformType and ReliabilityCredibility are allowed.")

        matching_enum = next((record for record in enum_class if string in (record.value, record.name)), None)

        if matching_enum:
            if enum_class is ReliabilityCredibility:
                self.reliability_credibility = matching_enum
            elif enum_class is PlatformType:
                self.platform_type = matching_enum

    def find_identity(self, string: str):
        identity_mapping = {
            "Необхідно ідентифікувати": "00",
            "Невідомий": "01",
            "Вірогідно дружній": "02",
            "Дружній": "03",
            "Нейтральний": "04",
            "Підозрілий": "05",
            "Ворожий": "06"
        }

        for key, value in identity_mapping.items():
            if re.search(key, string, re.IGNORECASE):
                self.sidc = self.sidc[:2] + value + self.sidc[4:]
                return

    def find_condition(self, string: str):
        condition_mapping = {
            "Присутній": "0",
            "Очікуваний": "1",
            "Ймовірний": "1",
            "Повністю": "2",
            "Частково": "3",
            "Небоєздатний": "4",
            "Відновлений": "5"
        }

        for key, value in condition_mapping.items():
            if re.search(key, string, re.IGNORECASE):
                self.sidc = self.sidc[:6] + value + self.sidc[7:]
                return

    def to_feature(self):
        builder = FeatureBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()

    def to_placemark(self):
        builder = PlacemarkBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()
    
    def to_placemark_str(self):
        return etree.ElementTree.tostring(self.to_placemark())
    
    def to_csv_line(self) -> dict:
        builder = CSVBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()
    
    def to_nvg(self):
        builder = NVGBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()


@dataclass
class Point(Geometry):
    coordinates: List[float]

    @property
    def geometry_type(self):
        return "Point"

    @property
    def default_sidc(self):
        return "10012500001313000000"


@dataclass
class Line(Geometry):
    coordinates: List[List[float]]

    @property
    def geometry_type(self):
        return "LineString"

    @property
    def default_sidc(self):
        return "10016600001100000000"


@dataclass
class Polygon(Geometry):
    coordinates: List[List[List[float]]]

    @property
    def geometry_type(self):
        return "Polygon"

    @property
    def default_sidc(self):
        return "10012500001501000000"


def _create_kml(geometries: Iterable[Geometry], add_styles: bool=False, folder_kmz_path: Union[None, str]=None) -> etree._Element:
    kml: etree._Element = etree.Element("kml", attrib={}, nsmap={None: "http://www.opengis.net/kml/2.2"})
    document: etree._Element = etree.SubElement(kml, "Document", attrib={}, nsmap={})

    for geometry in geometries:
        placemark = geometry.to_placemark()
        if add_styles and folder_kmz_path:
            unique_image_id = uuid.uuid4()
            png_file_name = f"{folder_kmz_path}/files/{unique_image_id}.png"

            # get feature sidc if it is not already set, use default
            if isinstance(geometry, Point):
                sidc = geometry.sidc if geometry.sidc else geometry.default_sidc
                # fix bug with sidc
                save_svg_as_png(sidc, png_file_name)
                add_style_to_document(document, unique_image_id)
                add_style_url_to_placemark(placemark, unique_image_id)
        document.append(placemark)

    return kml


class GeometriesList:
    def __init__(self):
        self.geometries: List[Geometry] = []

    def get_points(self) -> List[Point]:
        return [geom for geom in self.geometries if isinstance(geom, Point)]

    def get_lines(self) -> List[Line]:
        return [geom for geom in self.geometries if isinstance(geom, Line)]

    def get_polygons(self) -> List[Polygon]:
        return [geom for geom in self.geometries if isinstance(geom, Polygon)]

    def add_geometry(self, geometry: Geometry):
        if not isinstance(geometry, Geometry):
            raise ValueError("Only Geometry objects can be added.")
        self.geometries.append(geometry)

    def remove_geometry(self, geometry: Geometry):
        self.geometries.remove(geometry)

    def find_by_name(self, name: str) -> Optional[Geometry]:
        for geometry in self.geometries:
            if geometry.name == name:
                return geometry
        return None

    def get_all_geometries(self) -> List[Geometry]:
        return self.geometries

    def count_geometries(self) -> int:
        return len(self.geometries)

    def remove_duplicates(self, fields: List[str]):
        def make_hashable(value):
            if isinstance(value, list):
                return tuple(make_hashable(v) for v in value)
            return value

        seen = set()
        unique_geometries = []

        for geometry in self.geometries:
            comparison_tuple = tuple(make_hashable(getattr(geometry, attr)) for attr in fields)
            if comparison_tuple not in seen:
                seen.add(comparison_tuple)
                unique_geometries.append(geometry)

        self.geometries = unique_geometries

    def find_outline_colors(self):
        finder = ColorFinder()
        for geometry in self.geometries:
            concat_string = ''.join(filter(None, [geometry.name, *(geometry.comments or []), geometry.outline_color]))
            if concat_string:
                geometry.find_outline_color(concat_string, finder)

    def find_sidcs(self):
        for geometry in self.geometries:
            geometry.find_sidc()

    def save_geojson(self, folder_path, base_file_name, chunk_size=2000):
        for i, chunk_data in enumerate(batched(self.to_features(), chunk_size)):
            geojson_chunk = {
                "type": "FeatureCollection",
                "features": chunk_data
            }
            chunk_file_name = f"{base_file_name}-part-{i + 1}.geojson"
            full_path = f"{folder_path}/{chunk_file_name}"
            with open(full_path, 'w', encoding='utf-8') as file:
                json.dump(geojson_chunk, file, ensure_ascii=False, indent=4)

    def save_kml(self, folder_path: str, base_file_name: str, chunk_size=2000) -> None:
        for i, chunk_data in enumerate(batched(self.geometries, chunk_size)):
            kml: etree._Element = _create_kml(chunk_data)
            kml_string: bytes = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding="UTF-8")
            chunk_file_name = f"{base_file_name}-part-{i + 1}.kml"
            full_path = f"{folder_path}/{chunk_file_name}"
            with open(full_path, 'wb') as file:
                file.write(kml_string)

    def save_kmz(self, folder_path: str, base_file_name:str, chunk_size=2000) -> None:
        for i, chunk_data in enumerate(batched(self.geometries, chunk_size)):
            folder_kmz_path: str = f"{folder_path}/{base_file_name}-part-{i + 1}"
            os.makedirs(folder_kmz_path, exist_ok=True)
            os.makedirs(f'{folder_kmz_path}/files', exist_ok=True)
            kml: etree._Element = _create_kml(chunk_data, add_styles=True, folder_kmz_path=folder_kmz_path)
            save_kml_document(kml, folder_kmz_path, base_file_name, i + 1)
            create_kmz_archive(folder_kmz_path, folder_path, base_file_name, i + 1)

    def save_csv(self, folder_path: str, base_file_name:str, chunk_size=2000) -> None:
        for i, chunk_data in enumerate(batched(self.to_csv_line(), chunk_size)):
            headers = set()
            for line in chunk_data:
                headers.update(line.keys())

            chunk_file_name = f"{base_file_name}-part-{i + 1}.csv"
            full_path = f"{folder_path}/{chunk_file_name}"

            with open(full_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=sorted(headers)) # sort fieldnames to make sure the order is stable
                writer.writeheader()
                writer.writerows(chunk_data)

    def save_nvg(self, folder_path: str, base_file_name: str, chunk_size=2000) -> None:
        for i, chunk_data in enumerate(batched(self.to_nvg_elements(), chunk_size)):
            namespaces = {
                None: "https://org.c4isr.delta/nvg/extension",
                "ns2": "https://tide.act.nato.int/schemas/2012/10/nvg",
                "ns3": "http://purl.org/dc/elements/1.1/",
                "ns4": "http://purl.org/dc/terms/"
            }
            root = etree.Element("{%s}nvg" % namespaces["ns2"], nsmap=namespaces)
            
            for element in chunk_data:
                root.append(element)
            
            chunk_file_name = f"{base_file_name}-part-{i + 1}.nvg"
            full_path = f"{folder_path}/{chunk_file_name}"
            
            with open(full_path, 'wb') as file:
                file.write(etree.tostring(
                    root, 
                    pretty_print=True, 
                    xml_declaration=True, 
                    encoding="UTF-8"
                ))

    def to_features(self):
        return [geometry.to_feature() for geometry in self.geometries]

    def to_placemarks(self):
        return [geometry.to_placemark() for geometry in self.geometries]
    
    def to_csv_line(self):
        return [geometry.to_csv_line() for geometry in self.geometries]
    
    def to_nvg_elements(self):
        return [geometry.to_nvg() for geometry in self.geometries]

    def __str__(self):
        return "\n".join(str(geometry) for geometry in self.geometries)

    def __iter__(self):
        return iter(self.geometries)

    def __len__(self):
        return len(self.geometries)

    def __contains__(self, item):
        return item in self.geometries
