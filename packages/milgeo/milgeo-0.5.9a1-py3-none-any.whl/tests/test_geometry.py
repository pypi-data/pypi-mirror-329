from typing import List

import pytest
from text_to_sidc.austrian import PatternDict

from milgeo import GeometriesList, Point, Line, Polygon, PlatformType, ReliabilityCredibility, Config


@pytest.mark.parametrize("name, coordinates, geometry_type, sidc, fill_color, fill_opacity, "
                         "observation_datetime, quantity, expected_exception", [
                             ("Valid input", [0, 0], "Point", "12345678901234567890", "#ff0000", "0.5", None, None,
                              None),
                             ("Invalid SIDC length", [0, 0], "Point", "123456", None, None, None, None, ValueError),
                             ("Invalid fill color", [0, 0], "Point", None, "not_a_color", None, None, None, ValueError),
                             ("Invalid fill opacity", [0, 0], "Point", None, "#ff0000ff", "2", None, None, ValueError),
                             ("Invalid observation datetime", [0, 0], "Point", None, None, None, "2020-13-01T00:00:00",
                              None,
                              ValueError),
                             ("Invalid quantity", [0, 0], "Point", None, None, None, None, "12.5", ValueError),
                             ("Empty coordinates", [], "Point", None, None, None, None, None, ValueError),
                             (
                                     "Invalid Polygon coordinates", [[[0, 0], [1, 1]]], "Polygon", None, None, None,
                                     None, None,
                                     ValueError),
                             ("Invalid Polygon LinearRing", [[[0, 0], [1, 1], [2, 2], [3, 3]]], "Polygon", None, None,
                              None, None, None, ValueError),
                             ("Invalid LineString coordinates", [[0, 0]], "LineString", None, None, None, None, None,
                              ValueError),
                         ])
def test_geometry_post_init(name, coordinates, sidc, geometry_type, fill_color, fill_opacity,
                            observation_datetime, quantity, expected_exception):
    geometry_class = None
    if geometry_type == "Polygon":
        geometry_class = Polygon
    elif geometry_type == "Point":
        geometry_class = Point
    elif geometry_type == "LineString":
        geometry_class = Line
    assert geometry_class is not None
    if expected_exception:
        with pytest.raises(expected_exception):
            geometry_class(
                name=name,
                coordinates=coordinates,
                sidc=sidc,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                observation_datetime=observation_datetime,
                quantity=quantity
            )
    else:
        geom = geometry_class(
            name=name,
            coordinates=coordinates,
            sidc=sidc,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            observation_datetime=observation_datetime,
            quantity=quantity
        )
        assert geom.name == name
        assert geom.coordinates == coordinates
        assert geom.sidc == sidc
        assert geom.fill_color == fill_color
        assert geom.fill_opacity == fill_opacity
        assert geom.observation_datetime == observation_datetime
        assert geom.quantity == quantity


@pytest.mark.parametrize("geometries, fields, expected_names", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Point(name="Point", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
            ],
            ["name", "coordinates"],
            ["Point", "Line", "Polygon"]
    ),
    (
            [
                Point(name="FirstPoint", coordinates=[1.0, 2.0]),
                Point(name="SecondPoint", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
            ],
            ["name"],
            ["FirstPoint", "SecondPoint", "Line"]
    )
])
def test_remove_duplicates(geometries, fields, expected_names):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    geometries_list.remove_duplicates(fields)

    result_names = [geom.name for geom in geometries_list.get_all_geometries()]
    assert result_names == expected_names


@pytest.mark.parametrize("geometries, name_to_find, expected_geometry", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
            ],
            "Point",
            Point(name="Point", coordinates=[1.0, 2.0])
    ),
    (
            [
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
            ],
            "Line",
            Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]])
    )
])
def test_find_by_name(geometries, name_to_find, expected_geometry):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    result_geometry = geometries_list.find_by_name(name_to_find)
    assert result_geometry == expected_geometry


@pytest.mark.parametrize("geometries, expected_count", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
            ],
            3
    ),
    (
            [
                Point(name="FirstPoint", coordinates=[1.0, 2.0]),
                Point(name="SecondPoint", coordinates=[3.0, 4.0]),
            ],
            2
    )
])
def test_count_geometries(geometries, expected_count):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    assert geometries_list.count_geometries() == expected_count


@pytest.mark.parametrize("geometry, input_string, expected_sidc", [
    (Point(name="Point", coordinates=[1.0, 2.0]), "Невідомий", "10012500001313000000"),
    (Point(name="Point", coordinates=[1.0, 2.0]), "Дружній", "10032500001313000000"),
    (Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]), "Ворожий", "10066600001100000000"),
    (Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]), "Підозрілий",
     "10052500001501000000"),
])
def test_find_identity(geometry, input_string, expected_sidc):
    geometry.find_identity(input_string)
    assert geometry.sidc == expected_sidc


@pytest.mark.parametrize("geometry, input_string, expected_sidc", [
    (Point(name="Point", coordinates=[1.0, 2.0]), "Присутній", "10012500001313000000"),
    (Point(name="Point", coordinates=[1.0, 2.0]), "Очікуваний", "10012510001313000000"),
    (Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]), "Частково боєздатний", "10016630001100000000"),
    (Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
     "Відновлений до повної боєздатності", "10012550001501000000"),
])
def test_find_condition(geometry, input_string, expected_sidc):
    geometry.find_condition(input_string)
    assert geometry.sidc == expected_sidc


@pytest.mark.parametrize("enum_class, string, expected_result, field_name", [
    # Test matching by value (Ukrainian descriptions)
    (PlatformType, "Військовополонений (Впл)", PlatformType.POW, "platform_type"),
    (PlatformType, "Супутники (Супут)", PlatformType.SAT, "platform_type"),

    # Test matching by enum member name
    (PlatformType, "POW", PlatformType.POW, "platform_type"),
    (PlatformType, "SAT", PlatformType.SAT, "platform_type"),

    # Test matching by value for ReliabilityCredibility
    (ReliabilityCredibility, "A1", ReliabilityCredibility.A1, "reliability_credibility"),
    (ReliabilityCredibility, "F6", ReliabilityCredibility.F6, "reliability_credibility"),

    # Test matching by enum member name for ReliabilityCredibility
    (ReliabilityCredibility, "A1", ReliabilityCredibility.A1, "reliability_credibility"),
    (ReliabilityCredibility, "F6", ReliabilityCredibility.F6, "reliability_credibility"),

    # Invalid value cases
    (PlatformType, "invalid_value", None, "platform_type"),
    (ReliabilityCredibility, "invalid_value", None, "reliability_credibility"),
])
def test_set_enum_field(enum_class, string, expected_result, field_name):
    obj = Point(name="Point", coordinates=[1.0, 2.0])
    obj.map_enum_field(enum_class, string)
    assert getattr(obj, field_name) == expected_result


def test_invalid_enum_class():
    obj = Point(name="Point", coordinates=[1.0, 2.0])
    with pytest.raises(ValueError, match="Invalid class. Only PlatformType and ReliabilityCredibility are allowed."):
        obj.map_enum_field(str, "some_value")


@pytest.mark.parametrize("geometry, expected_sidc", [
    (Point(name="танк", coordinates=[1.0, 2.0]), '10061500001202000000'),
    (Point(name="сау", coordinates=[1.0, 2.0]), '10061500331109000000'),
    (Point(name="мон", coordinates=[1.0, 2.0]), '10061500002102000000'),
    (Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]]), '10016600001100000000'),
    (Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]), '10012500001501000000')
])
def test_find_sidc(geometry, expected_sidc):
    geometry.find_sidc()
    assert geometry.sidc == expected_sidc


@pytest.mark.parametrize("geometry, expected_sidc, expected_name", [
    (Point(name='', coordinates=[1.0, 2.0], comments=['танк']), '10061500001202000000', 'танк'),
    (Point(name='', coordinates=[1.0, 2.0], comments=['сау']), '10061500331109000000', 'сау'),
    (Point(name='', coordinates=[1.0, 2.0], comments=['мон']), '10061500002102000000', 'мон'),
    (Line(name='', coordinates=[[1.0, 2.0], [3.0, 4.0]], comments=['сау']), '10016600001100000000', ''),
    (Polygon(name='', coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]], comments=['Polygon']), '10012500001501000000', '')
])
def test_find_sidc_with_comments(geometry, expected_sidc, expected_name):
    Config().set_sidc_from_comments(True)
    geometry.find_sidc()
    assert geometry.sidc == expected_sidc
    assert geometry.name == expected_name


@pytest.mark.parametrize("geometry, expected_sidc", [
    (Point(name="танк", coordinates=[1.0, 2.0]), '10061500001202000000'),
    (Point(name="test", coordinates=[1.0, 2.0]), '000000000000000000000'),
    (Point(name="noname", coordinates=[1.0, 2.0]), '000000000000000000000'),
    (Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]]), '10016600001100000000'),
    (Polygon(name="АТ", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]), '10012500001501000000')
])
def test_find_sidc_with_default_sidc(geometry, expected_sidc):
    Config().add_default_sidc("000000000000000000000")
    geometry.find_sidc()
    assert geometry.sidc == expected_sidc


@pytest.mark.parametrize("geometry, expected_sidc", [
    (Point(name="танк", coordinates=[1.0, 2.0]), '1111111111111111'),
    (Point(name="сау", coordinates=[1.0, 2.0]), '2222222222222222'),
    (Point(name="мон", coordinates=[1.0, 2.0]), '2222222222222222'),
    (Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]]), '10016600001100000000'),
    (Polygon(name="АТ", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]), '10012500001501000000')
])

def test_find_sidc_with_custom_patterns(geometry, expected_sidc):
    patterns: List[PatternDict] = [
        {"sidc": '1111111111111111', "list_of_patterns": ['танк']},
        {"sidc": '2222222222222222', "list_of_patterns": ['мон', 'сау']}
    ]

    Config().add_custom_patterns(patterns)
    geometry.find_sidc()
    assert geometry.sidc == expected_sidc

@pytest.mark.parametrize("geometry, expected_sidc", [
    (Point(name="танк", coordinates=[1.0, 2.0], sidc=''), '10012500001313000000'),
    (Point(name="танк", coordinates=[1.0, 2.0], sidc=None), '10012500001313000000'),
    (Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]], sidc=''), '10016600001100000000'),
    (Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]], sidc=None), '10016600001100000000'),
    (Polygon(name="АТ", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]], sidc=""), '10012500001501000000'),
    (Polygon(name="АТ", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]], sidc=None), '10012500001501000000')

])

def test_point_with_empty_sidc(geometry, expected_sidc):
    assert geometry.sidc == expected_sidc


@pytest.mark.parametrize("sidc", [
    "333fg",  # Empty string
    "123",  # Less than 20 characters
    "123456789012345678901"  # More than 20 characters
])
def test_sidc_number_of_char_validation(sidc):
    with pytest.raises(ValueError, match="sidc must be exactly 20 digits."):
        Point(name='Infantry', sidc=sidc, coordinates=[31, 53], staff_comments='dfd', 
              quantity="5", direction="45", speed='10')

def test_save_features_in_chunks(tmp_path):
    geometries_list = GeometriesList()
    point = Point(name="Point1", coordinates=[1.0, 2.0])
    geometries_list.add_geometry(point)
    folder_path = tmp_path / "features"
    folder_path.mkdir()
    geometries_list.save_geojson(str(folder_path), "test_features", chunk_size=1)
    assert (folder_path / "test_features-part-1.geojson").exists()


def test_save_placemarks_in_chunks(tmp_path):
    geometries_list = GeometriesList()
    point = Point(name="Point1", coordinates=[1.0, 2.0])
    geometries_list.add_geometry(point)
    folder_path = tmp_path / "placemarks"
    folder_path.mkdir()
    geometries_list.save_kml(str(folder_path), "test_placemarks", chunk_size=1)
    assert (folder_path / "test_placemarks-part-1.kml").exists()


def test_save_placemarks_in_multiple_chunks_as_kmz(tmp_path):
    geometries_list = GeometriesList()
    point = Point(name="Point1", coordinates=[1.0, 2.0])
    geometries_list.add_geometry(point)
    geometries_list.add_geometry(point)
    folder_path = tmp_path / "placemarks_kmz"
    folder_path.mkdir()
    geometries_list.save_kmz(str(folder_path), "test_placemarks", chunk_size=1)
    assert (folder_path / "test_placemarks-part-1.kmz").exists()
    assert (folder_path / "test_placemarks-part-2.kmz").exists()



def test_save_different_geometries_in_chunks_as_kmz(tmp_path):
    geometries_list = GeometriesList()
    point = Point(name="Point1", coordinates=[1.0, 2.0])
    line = Line(name="сау", coordinates=[[1.0, 2.0], [3.0, 4.0]])
    polygon = Polygon(name="АТ", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])

    geometries_list.add_geometry(point)
    geometries_list.add_geometry(line)
    geometries_list.add_geometry(polygon)

    folder_path = tmp_path / "placemarks_kmz"
    folder_path.mkdir()
    geometries_list.save_kmz(str(folder_path), "test_placemarks", chunk_size=5)
    assert (folder_path / "test_placemarks-part-1.kmz").exists()
