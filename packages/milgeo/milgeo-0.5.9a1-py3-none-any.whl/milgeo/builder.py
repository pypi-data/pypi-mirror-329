import copy
from enum import Enum
import json
from typing import Dict, Any
from lxml.etree import Element, SubElement
import uuid
from lxml.etree import ElementTree

from milgeo.color import ColorFinder


class FeatureBuilder:
    def __init__(self, geometry):
        self.geometry = geometry
        self.feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {}
        }

    def add_basic_elements(self):
        self.feature["properties"]["name"] = self.geometry.name \
            if self.geometry.name \
            else ''
        self.feature["properties"]["sidc"] = self.geometry.sidc \
            if self.geometry.sidc is not None \
            else self.geometry.default_sidc
        self.feature["properties"]["comments"] = []

    def add_optional_properties(self):
        properties = [
            "observation_datetime",
            "reliability_credibility",
            "staff_comments",
            "platform_type",
            "quantity",
            "direction",
            "speed",
            "outline-color",
            "fill_color",
            "fill_opacity",
            "comments"
        ]
        for prop in properties:
            if prop == "outline-color":
                attr_name = "outline_color"
            else:
                attr_name = prop
            value = getattr(self.geometry, attr_name, None)
            if value is not None:
                if isinstance(value, Enum):
                    value = value.name
                self.feature["properties"][prop] = value

    def add_geometry(self):
        self.feature["geometry"] = dict(type=self.geometry.geometry_type, coordinates=self.geometry.coordinates)

    def build(self) -> Dict[str, Any]:
        return self.feature


class PlacemarkBuilder:
    def __init__(self, geometry):
        self.geometry = geometry
        self.placemark = Element("Placemark")

    def add_basic_elements(self):
        name = SubElement(self.placemark, "name")
        sidc = SubElement(self.placemark, "sidc")

        name.text = self.geometry.name
        sidc.text = self.geometry.sidc
        

    def add_optional_properties(self):
        style = None
        if self.geometry.outline_color:
            style = SubElement(self.placemark, "Style")
            line_style = SubElement(style, "LineStyle")
            color = SubElement(line_style, "color")
            color.text = self.geometry.outline_color
        
        if self.geometry.fill_color:
            style = style if style is not None else SubElement(self.placemark, "Style")
            poly_style = SubElement(style, "PolyStyle")
            color = SubElement(poly_style, "color")
            fill_opacity= self.geometry.fill_opacity if self.geometry.fill_opacity is not None else 1.0
            color.text = ColorFinder.make_argb_color(self.geometry.fill_color, fill_opacity)

        properties = [
            "observation_datetime",
            "reliability_credibility",
            "staff_comments",
            "platform_type",
            "quantity",
            "direction",
            "speed",
            "comments"
        ]

        extended_data = SubElement(self.placemark, "ExtendedData")

        for prop in properties:
            value = getattr(self.geometry, prop, None)
            if value is not None:
                if isinstance(value, Enum):
                    value = value.name
                if isinstance(value, list):
                    value = "\n".join([str(v) for v in value])
                
                data_el = SubElement(extended_data, "Data")
                data_el.set("name", prop)
                value_el = SubElement(data_el, "value")
                value_el.text = str(value)


    def add_geometry(self):
        if self.geometry.geometry_type == "Point":
            self._add_point()
        elif self.geometry.geometry_type == "LineString":
            self._add_line_string()
        elif self.geometry.geometry_type == "Polygon":
            self._add_polygon()

    def _add_point(self):
        geometry_element = SubElement(self.placemark, "Point")
        coordinates = SubElement(geometry_element, "coordinates")
        coordinates.text = f"{self.geometry.coordinates[0]},{self.geometry.coordinates[1]}"

    def _add_line_string(self):
        geometry_element = SubElement(self.placemark, "LineString")
        coordinates = SubElement(geometry_element, "coordinates")
        coordinates.text = " ".join([f"{coord[0]},{coord[1]}" for coord in self.geometry.coordinates])

    def _add_polygon(self):
        geometry_element = SubElement(self.placemark, "Polygon")
        outer_boundary_is = SubElement(geometry_element, "outerBoundaryIs")
        linear_ring = SubElement(outer_boundary_is, "LinearRing")
        coordinates = SubElement(linear_ring, "coordinates")
        coordinates.text = " ".join([f"{coord[0]},{coord[1]}" for ring in self.geometry.coordinates for coord in ring])

    def build(self):
        return copy.deepcopy(self.placemark)


class CSVBuilder:
    def __init__(self, geometry):
        self.geometry = geometry
        self.csv_features = {}

    def add_basic_elements(self):
        self.csv_features["name"] = self.geometry.name or ''
        self.csv_features["sidc"] = self.geometry.sidc or self.geometry.default_sidc

    def add_optional_properties(self):
        csv_props_to_geometry_props = {
            "id": "id",
            "observation_datetime": "observation_datetime",
            "reliability_credibility": "reliability_credibility",
            "staff_comments": "staff_comments",
            "platform_type": "platform_type",
            "quantity": "quantity",
            "direction": "direction",
            "speed": "speed",
            "outline-color": "outline_color",
            "fill-color": "fill_color",
            "fill-opacity": "fill_opacity",
        }
        for csv_prop, geometry_prop in csv_props_to_geometry_props.items():
            value = getattr(self.geometry, geometry_prop, None)
            if value is None:
                continue
            if isinstance(value, Enum):
                value = value.name
            self.csv_features[csv_prop] = value

        if self.geometry.comments:
            for i, comment in enumerate(self.geometry.comments):
                self.csv_features[f"comment {i+1}"] = comment
            
        if self.geometry.metadata:
            for key, value in self.geometry.metadata.items():
                self.csv_features[f"milgeo:meta:{key}"] = json.dumps(value)

    def add_geometry(self):
        if self.geometry.geometry_type == "Point":
            self._add_point()
        elif self.geometry.geometry_type == "LineString":
            self._add_line_string()
        elif self.geometry.geometry_type == "Polygon":
            self._add_polygon()

    def _add_point(self):
        if len(self.geometry.coordinates) == 3:
            x, y, z = self.geometry.coordinates
            self.csv_features['coordinates'] = f'POINT Z ({x} {y} {z})'
        else:
            x, y = self.geometry.coordinates
            self.csv_features['coordinates'] = f'POINT ({x} {y})'

    def _add_line_string(self):
        if all(len(coord) == 3 for coord in self.geometry.coordinates):
            interal_coords = ", ".join([f"{coord[0]} {coord[1]} {coord[2]}" for coord in self.geometry.coordinates])    
            self.csv_features['coordinates'] = f'LINESTRING Z ({interal_coords})'
        else:
            interal_coords = ", ".join([f"{coord[0]} {coord[1]}" for coord in self.geometry.coordinates])    
            self.csv_features['coordinates'] = f'LINESTRING ({interal_coords})'

    def _add_polygon(self):
        if self.geometry.coordinates[0] != self.geometry.coordinates[-1]: # close polygon
            self.geometry.coordinates.append(self.geometry.coordinates[0])

        if all(len(coord) == 3 for coord in self.geometry.coordinates):
            interal_coords = ", ".join([f"{coord[0]} {coord[1]} {coord[2]}" for ring in self.geometry.coordinates for coord in ring])
            self.csv_features['coordinates'] = f'POLYGON Z (({interal_coords}))'
        else:
            interal_coords = ", ".join([f"{coord[0]} {coord[1]}" for ring in self.geometry.coordinates for coord in ring])
            self.csv_features['coordinates'] = f'POLYGON (({interal_coords}))'
    
    def build(self) -> dict:
        return self.csv_features


class NVGBuilder:    
    def __init__(self, geometry):
        self.geometry = geometry
        self.delta_ns = "https://org.c4isr.delta/nvg/extension"
        self.namespaces = {
            None: "https://org.c4isr.delta/nvg/extension",
            "ns2": "https://tide.act.nato.int/schemas/2012/10/nvg",
            "ns3": "http://purl.org/dc/elements/1.1/",
            "ns4": "http://purl.org/dc/terms/"
        }
        
        if self.geometry.geometry_type == "Point":
            self.element = Element("{%s}point" % self.namespaces["ns2"], nsmap=self.namespaces)
        elif self.geometry.geometry_type == "LineString":
            self.element = Element("{%s}polyline" % self.namespaces["ns2"], nsmap=self.namespaces)
        elif self.geometry.geometry_type == "Polygon":
            self.element = Element("{%s}polygon" % self.namespaces["ns2"], nsmap=self.namespaces)
        else:
            raise ValueError(f"Unsupported geometry type: {self.geometry.geometry_type}")

    def add_basic_elements(self):
        uri = f"urn:guid:{self.geometry.id or str(uuid.uuid4())}"
        self.element.set("uri", uri)
        self.element.set("symbol", f"app6d:{self.geometry.sidc or self.geometry.default_sidc}")
        self.element.set("label", self.geometry.name)
        
        modifiers = f"T:{self.geometry.name};"
        
        if hasattr(self.geometry, 'outline_color') and self.geometry.outline_color:
            rgba_color = ColorFinder.make_rgba_color(self.geometry.outline_color)
            if rgba_color:
                modifiers += f"DELTA_COLOR:{rgba_color};"
        
        if hasattr(self.geometry, 'reliability_credibility') and self.geometry.reliability_credibility:
            modifiers += f"J:{self.geometry.reliability_credibility.name};"
            
        if hasattr(self.geometry, 'quantity') and self.geometry.quantity:
            modifiers += f"C:{self.geometry.quantity};"
            
        if hasattr(self.geometry, 'platform_type') and self.geometry.platform_type:
            modifiers += f"AD:{self.geometry.platform_type.name};"
            
        self.element.set("modifiers", modifiers)

    def add_optional_properties(self):
        extended_data = SubElement(self.element, "{%s}ExtendedData" % self.namespaces["ns2"])
        extended_data.set("schemaRef", "#delta-schema")
        
        metadata_fields = {}
        
        if hasattr(self.geometry, 'observation_datetime') and self.geometry.observation_datetime:
            metadata_fields["delta:MIM:b28560ab-1fa6-4134-8ec0-09ab7c19785d"] = self.geometry.observation_datetime
    
        if hasattr(self.geometry, 'reliability_credibility') and self.geometry.reliability_credibility:
            metadata_fields["delta:MIM:05fca33a-2865-4293-98b8-1e759bc81e7d"] = "UnspecifiedSensitiveSource"
        
        for key, value in metadata_fields.items():
            simple_data = SubElement(extended_data, "{%s}SimpleData" % self.namespaces["ns2"])
            simple_data.set("key", key)
            simple_data.text = value
        
        text_info = SubElement(self.element, "{%s}textInfo" % self.namespaces["ns2"])
        if hasattr(self.geometry, 'comments') and self.geometry.comments:
            text_info.text = "\n".join(self.geometry.comments)

    def add_geometry(self):
        if self.geometry.geometry_type == "Point":
            x, y = self.geometry.coordinates
            self.element.set("x", str(x))
            self.element.set("y", str(y))
        elif self.geometry.geometry_type == "LineString" or self.geometry.geometry_type == "Polygon":
            if self.geometry.geometry_type == "LineString":
                points = " ".join([f"{coord[0]},{coord[1]}" for coord in self.geometry.coordinates])
            else:
                points = " ".join([f"{coord[0]},{coord[1]}" for coord in self.geometry.coordinates[0]])
            
            self.element.set("points", points)

    def build(self):
        return copy.deepcopy(self.element)
        