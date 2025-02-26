from dataclasses import dataclass, field
import datetime
import io
import pytest

from lxml import etree
from lxml import objectify
from lxml.objectify import ObjectifiedElement as KMLElement
import svgpathtools as svg

from milgeo.config import Config
from milgeo.extractor import ExtractorContext, GeometryExtractor, InvalidPasswordError
from milgeo.geometry import Line, Point, Polygon
from milgeo.kropyva.tactics.extractor import TacticsExtractor
from milgeo.kropyva.tactics.low_level import LatLonBox
import milgeo.kropyva.tactics.low_level as low_level
import milgeo.kropyva.tactics.high_level as high_level
from milgeo.utils.kme_utils import write_kml_as_kme
from milgeo.utils.svg_utils import SVGCoords
import milgeo.utils.svg_utils as svg_utils
from milgeo.utils.coords import WGSCoords


@pytest.mark.parametrize("coord_pair, lat_lon_box, expected_result", [
    (WGSCoords(y=47.0000, x=35.0000), LatLonBox(north=47.0050, south=47, east=35.01, west=35), SVGCoords(x=0, y=1000)),
    (WGSCoords(y=47.0050, x=35.0050), LatLonBox(north=47.0050, south=47, east=35.01, west=35), SVGCoords(x=500, y=0)),
    (WGSCoords(y=47.0025, x=35.0100), LatLonBox(north=47.0050, south=47, east=35.01, west=35), SVGCoords(x=1000, y=500)),
])
def test_to_svg_coord_pair(coord_pair, lat_lon_box, expected_result):
    # check equality with precision of 1e-6
    (x, y) = svg_utils.to_svg_coord_pair(coord_pair, lat_lon_box).xy
    (expected_x, expected_y) = expected_result.xy
    assert round(x, 6) == round(expected_x, 6)
    assert round(y, 6) == round(expected_y, 6)

@pytest.mark.parametrize("points, lat_lon_box, closed, expected_result", [
    (
        [WGSCoords(y=47.0000, x=35.0000), WGSCoords(y=47.0050, x=35.0050)],
        None,
        False,
        svg.parse_path("M 0.0,1000.0 L 1000.0,0.0")
    ),
    (
        [WGSCoords(y=47.0000, x=35.0000), WGSCoords(y=47.0050, x=35.0050)],
        LatLonBox(north=47.0050, south=47, east=35.01, west=35),
        False,
        svg.parse_path("M 0.0,1000.0 L 500.0,0.0")
    ),
    (
        [WGSCoords(y=47.0025, x=35.0025), WGSCoords(y=47.0050, x=35.0050)],
        LatLonBox(north=47.0050, south=47, east=35.01, west=35),
        True,
        svg.parse_path("M 250.0,500.0 L 500.0,0.0 Z")
    ),
])
def test_encode_svg_linestring(points, lat_lon_box, closed, expected_result):
    assert svg_utils.to_svg_path(points, lat_lon_box, closed) == expected_result

def test_kml_text():
    text = low_level.KMLText(text="Test", x=10, y=20)
    kml = text.to_kml()

    assert kml.tag == '{http://www.opengis.net/kml/2.2}text'
    assert kml.text == "Test"
    assert kml.attrib['x'] == "10"
    assert kml.attrib['y'] == "20"

    # check default values
    assert kml.attrib['fill'] == "black"
    assert 'bg' not in kml.attrib
    assert 'dx' not in kml.attrib
    assert 'dy' not in kml.attrib
    assert kml.attrib['font-family'] == "Arial"
    assert kml.attrib['font-size'] == "13"
    assert kml.attrib['text-anchor'] == "middle"
    assert kml.attrib['font-weight'] == "bold"
    assert kml.attrib['alignment-baseline'] == "text-before-edge"
    assert kml.attrib['anchor-style'] == "none"

def test_kml_icon():
    icon = low_level.KMLIcon(href="Міна", width=10, height=20)
    kml = icon.to_kml()

    assert kml.tag == '{http://www.opengis.net/kml/2.2}use'
    assert kml.attrib['href'] == "Міна"
    assert kml.attrib['width'] == "10"
    assert kml.attrib['height'] == "20"
    # check default values
    assert kml.attrib['stroke-width'] == "2"

@pytest.mark.parametrize("path_point_info, force_index, expected_types, expected_marker, expected_index", [
    (low_level.PathPointInfo(type={'a'}, marker='circle', index=0), None, ["a"], 'circle', "0"),
    (low_level.PathPointInfo(type={'b'}, marker='circle'), None, ["b"], 'circle', None),
    (low_level.PathPointInfo(type={'a', 'b'}, index=0), 1, ["a b", "b a"], None, "1"),
    (low_level.PathPointInfo(type={'a', 'b'}), 1, ["a b", "b a"], None, "1"),
])
def test_kml_path_point_info(path_point_info, force_index, expected_types, expected_marker, expected_index):
    kml = path_point_info.to_kml(index=force_index)
    assert kml.tag == '{http://www.opengis.net/kml/2.2}point'
    assert kml.attrib['type'] in expected_types
    if expected_marker:
        assert kml.attrib['marker'] == expected_marker
    else:
        assert 'marker' not in kml.attrib
    if expected_index:
        assert kml.attrib['index'] == expected_index
    else:
        assert 'index' not in kml.attrib
    

def test_kml_path():
    path = low_level.KMLPath(
        points=[
            low_level.PathPointInfo(type={'editable', 'custom'}, index=123123),
            low_level.PathPointInfo(type={'custom'}, marker='circle'),
        ],
        definition=svg.parse_path("M0,0 L100,100"),
    )
    kml = path.to_kml()

    assert kml.tag == '{http://www.opengis.net/kml/2.2}path'
    assert kml.attrib['d'] == "M 0.0,0.0 L 100.0,100.0"
    assert kml.countchildren() == 2 #type: ignore

    point0, point1 = kml.getchildren() #type: ignore
    assert point0.tag == '{http://www.opengis.net/kml/2.2}point'
    assert point0.attrib['type'] in ["custom editable", "editable custom"]
    assert point0.attrib['index'] == "0"
    assert 'marker' not in point0.attrib

    assert point1.tag == '{http://www.opengis.net/kml/2.2}point'
    assert point1.attrib['type'] == "custom"
    assert point1.attrib['marker'] == "circle"
    assert point1.attrib['index'] == "1"

@pytest.fixture
def sample_point_placemark():
    return high_level.Point(
        name='Назва',
        color='red',
        coords=WGSCoords(y=47.0, x=35.0),
        cls='!10031000141205',
        url='url(!10031000141205)',
        labels=[low_level.KMLText(text="Test", dx=10, dy=20)],
        underlying_icons=[low_level.KMLIcon(href="взвод", width=10, height=20)],
        creation_time=datetime.datetime(2024, 12, 25, 10, 36, 29),
    )

def test_point_placemark(sample_point_placemark):
    point = sample_point_placemark
    assert point.get_points() == [WGSCoords(y=47.0, x=35.0)]
    assert point.get_type() == "!10031000141205"
    assert point.get_items() == [
        low_level.KMLIcon(href="взвод", width=10, height=20),
        low_level.KMLIcon(href="url(!10031000141205)", width=30, height=30),
        low_level.KMLText(text="Test", dx=10, dy=20),
    ]

@pytest.mark.skip('checked in test_kml_document, uncomment to test points separately')
def test_point_placemark_kml(sample_point_placemark):
    expected_kml = '''<Placemark xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <name>Назва</name>
  <description></description>
  <Point>
    <coordinates>35.0,47.0</coordinates>
  </Point>
  <ExtendedData>
    <svg>
      <g cls="!10031000141205" stroke="red" time="2024-12-25T10:36:29">
        <use href="взвод" width="10" height="20" stroke-width="2"/>
        <use href="url(!10031000141205)" width="30" height="30" stroke-width="2"/>
        <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
      </g>
    </svg>
  </ExtendedData>
</Placemark>
'''
    actual_kml = etree.tostring(sample_point_placemark.to_kml(), pretty_print=True, encoding='unicode') #type: ignore
    assert actual_kml == expected_kml

@pytest.fixture
def sample_linestring_placemark():
    return high_level.LineString(
        name='Назва',
        color='red',
        coords=[
            WGSCoords(y=47.0, x=35.0),
            WGSCoords(y=47.0050, x=35.0050),
        ],
        cls='Лінія',
        labels=[low_level.KMLText(text="Test", dx=10, dy=20)],
        stroke_pattern="url(Пунктир)",
    )

def test_linestring_placemark(sample_linestring_placemark):
    linestring = sample_linestring_placemark
    assert linestring.get_points() == [
        WGSCoords(y=47.0, x=35.0),
        WGSCoords(y=47.0050, x=35.0050),
    ]
    assert linestring.get_type() == "Лінія"
    assert linestring.get_items() == [
        low_level.KMLPath(points=[
            low_level.PathPointInfo(type={'editable', 'custom'}, index=0),
            low_level.PathPointInfo(type={'editable', 'custom'}, index=1),
        ], definition=svg.parse_path("M0,1000 L1000,0")),
        low_level.KMLText(text="Test", dx=10, dy=20),
    ]
    assert linestring.stroke_pattern == "url(Пунктир)"

@pytest.mark.skip('checked in test_kml_document, uncomment to test linestrings separately')
def test_linestring_kml(sample_linestring_placemark):
    expected_kml = '''<Placemark xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <name>Назва</name>
  <description></description>
  <Point>
    <coordinates>35.0025,47.0025</coordinates>
  </Point>
  <ExtendedData>
    <svg>
      <g cls="Лінія" stroke="red" stroke-pattern="url(Пунктир)">
        <path d="M 0.0,1000.0 L 1000.0,0.0" stroke-width="2">
          <point index="0" type="custom editable"/>
          <point index="1" type="custom editable"/>
        </path>
        <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
      </g>
    </svg>
  </ExtendedData>
  <Region>
    <LatLonAltBox>
      <west>35.0</west>
      <east>35.005</east>
      <north>47.005</north>
      <south>47.0</south>
    </LatLonAltBox>
  </Region>
</Placemark>
'''
    actual_kml = etree.tostring(sample_linestring_placemark.to_kml(), pretty_print=True, encoding='unicode') #type: ignore
    assert actual_kml == expected_kml

@pytest.fixture
def sample_polygon_placemark():
    return high_level.Polygon(
        name='Назва',
        color='red',
        fill='blue',
        coords=[
            WGSCoords(y=47.0, x=35.0),
            WGSCoords(y=47.0050, x=35.0050),
            WGSCoords(y=47.0025, x=35.0100),
        ],
        cls='Опорний пункт',
        labels=[low_level.KMLText(text="Test", dx=10, dy=20)],
        stroke_pattern="url(Пунктир)",
    )

def test_polygon_placemark(sample_polygon_placemark):
    p = sample_polygon_placemark
    assert p.get_points() == [
        WGSCoords(y=47.0, x=35.0),
        WGSCoords(y=47.0050, x=35.0050),
        WGSCoords(y=47.0025, x=35.0100),
    ]
    assert p.get_type() == "Опорний пункт"
    assert p.get_items() == [
        low_level.KMLPath(points=[
            low_level.PathPointInfo(type={'editable', 'custom'}, index=0),
            low_level.PathPointInfo(type={'editable', 'custom'}, index=1),
            low_level.PathPointInfo(type={'editable', 'custom'}, index=2),
        ], definition=svg.parse_path("M0,1000 L500,0 L1000,500 Z")),
        low_level.KMLText(text="Test", dx=10, dy=20),
    ]

@pytest.mark.skip('checked in test_kml_document, uncomment to test polygons separately')
def test_polygon_kml(sample_polygon_placemark):
    expected_kml = '''<Placemark xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <name>Назва</name>
  <description></description>
  <Point>
    <coordinates>35.005,47.0025</coordinates>
  </Point>
  <ExtendedData>
    <svg>
      <g cls="Опорний пункт" stroke="red" fill="blue" stroke-pattern="url(Пунктир)">
        <path d="M 0.0,1000.0 L 500.0,0.0 L 1000.0,500.0 Z" stroke-width="2">
          <point index="0" type="custom editable"/>
          <point index="1" type="custom editable"/>
          <point index="2" type="custom editable"/>
        </path>
        <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
      </g>
    </svg>
  </ExtendedData>
  <Region>
    <LatLonAltBox>
      <west>35.0</west>
      <east>35.01</east>
      <north>47.005</north>
      <south>47.0</south>
    </LatLonAltBox>
  </Region>
</Placemark>
'''
    actual_kml = etree.tostring(sample_polygon_placemark.to_kml(), pretty_print=True, encoding='unicode') #type: ignore
    assert actual_kml == expected_kml

@pytest.fixture
def sample_text_placemark():
    return high_level.TextObject(
        name='Text object',
        coords=WGSCoords(x=35.7, y=47.4),
        label=low_level.KMLText(
            text='Біліна Етанол',
            dx=-87.0,
            dy=-3.0,
            font_size=20,
            bg='none',
            color='#FFA500',
        ),
        creation_time=datetime.datetime(2024, 12, 19, 15, 50, 30),
    )

sample_kml = '''<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document>
    <open>1</open>
    <name>Test</name>
    <Folder>
      <name>Subfolder</name>
      <Placemark>
        <name>Назва</name>
        <description></description>
        <Point>
          <coordinates>35.0,47.0</coordinates>
        </Point>
        <ExtendedData>
          <svg>
            <g cls="!10031000141205" stroke="red" time="2024-12-25T10:36:29">
              <use href="взвод" width="10" height="20" stroke-width="2"/>
              <use href="url(!10031000141205)" width="30" height="30" stroke-width="2"/>
              <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
            </g>
          </svg>
        </ExtendedData>
      </Placemark>
    </Folder>
    <Placemark>
      <name>Назва</name>
      <description></description>
      <Point>
        <coordinates>35.0025,47.0025</coordinates>
      </Point>
      <ExtendedData>
        <svg>
          <g cls="Лінія" stroke="red" stroke-pattern="url(Пунктир)">
            <path d="M 0.0,1000.0 L 1000.0,0.0" stroke-width="2">
              <point index="0" type="custom editable"/>
              <point index="1" type="custom editable"/>
            </path>
            <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
          </g>
        </svg>
      </ExtendedData>
      <Region>
        <LatLonAltBox>
          <west>35.0</west>
          <east>35.005</east>
          <north>47.005</north>
          <south>47.0</south>
        </LatLonAltBox>
      </Region>
    </Placemark>
    <Placemark>
      <name>Назва</name>
      <description></description>
      <Point>
        <coordinates>35.005,47.0025</coordinates>
      </Point>
      <ExtendedData>
        <svg>
          <g cls="Опорний пункт" stroke="red" fill="blue" stroke-pattern="url(Пунктир)">
            <path d="M 0.0,1000.0 L 500.0,0.0 L 1000.0,500.0 Z" stroke-width="2">
              <point index="0" type="custom editable"/>
              <point index="1" type="custom editable"/>
              <point index="2" type="custom editable"/>
            </path>
            <text fill="black" font-family="Arial" font-size="13" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="10" dy="20">Test</text>
          </g>
        </svg>
      </ExtendedData>
      <Region>
        <LatLonAltBox>
          <west>35.0</west>
          <east>35.01</east>
          <north>47.005</north>
          <south>47.0</south>
        </LatLonAltBox>
      </Region>
    </Placemark>
    <Placemark>
      <name>Non-kropyva kml</name>
      <description/>
      <LineString>
        <coordinates>35.0,47.0 35.005,47.005</coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Text object</name>
      <description></description>
      <Point>
        <coordinates>35.7,47.4</coordinates>
      </Point>
      <ExtendedData>
        <svg>
          <g cls="Текст" stroke="#FFA500" fill="none" time="2024-12-19T15:50:30">
            <text fill="#FFA500" bg="none" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" anchor-style="none" alignment-baseline="text-before-edge" dx="-87.0" dy="-3.0">Біліна Етанол</text>
          </g>
        </svg>
      </ExtendedData>
    </Placemark>
  </Document>
</kml>
'''

@pytest.fixture
def sample_kme():
    kme_path = 'tests/resources/test2.kme'
    with open(kme_path, 'wb') as f:
        write_kml_as_kme(sample_kml, 'Q1111', f)
    file = open(kme_path, 'rb')
    yield file
    file.close()

@pytest.fixture
def sample_non_tactic_placemark():
    return low_level.RawUnknownPlacemark(
        name='Non-kropyva kml',
        description='',
        raw_kml=objectify.fromstring('<Placemark><name>Non-kropyva kml</name><description/><LineString><coordinates>35.0,47.0 35.005,47.005</coordinates></LineString></Placemark>'),
    )

def test_kml_document(sample_point_placemark, sample_linestring_placemark, sample_polygon_placemark, sample_non_tactic_placemark, sample_text_placemark):
    doc = low_level.RawFolder(
        name='Test',
        placemarks=[sample_linestring_placemark, sample_polygon_placemark, sample_non_tactic_placemark, sample_text_placemark],
        subfolders=[low_level.RawFolder(name='Subfolder', placemarks=[sample_point_placemark])],
    )
    actual_kml = etree.tostring(doc.to_kml_document(), pretty_print=True, encoding='unicode') #type: ignore
    # with open('tests/test_kml_document.kml', 'w', encoding='utf-8') as f:
        # f.write(actual_kml)
    assert actual_kml == sample_kml

def test_parse_kml_document_low_level(sample_point_placemark, sample_linestring_placemark, sample_polygon_placemark, sample_text_placemark):
    doc = low_level.parse_kml_document(sample_kml)
    assert doc.name == 'Test'
    assert len(doc.placemarks) == 4
    assert len(doc.subfolders) == 1
    assert doc.subfolders[0].name == 'Subfolder'
    assert len(doc.subfolders[0].placemarks) == 1

    assert doc.placemarks[0] == sample_linestring_placemark.to_low_level()
    assert doc.placemarks[1] == sample_polygon_placemark.to_low_level()
    assert isinstance(doc.placemarks[2], low_level.RawUnknownPlacemark) and doc.placemarks[2].name == 'Non-kropyva kml'
    assert doc.placemarks[3] == sample_text_placemark.to_low_level()
    assert doc.subfolders[0].placemarks[0] == sample_point_placemark.to_low_level()

def test_parse_kml_document_high_level(sample_point_placemark, sample_linestring_placemark, sample_polygon_placemark, sample_text_placemark):
    parser = high_level.KMLParser()
    doc = parser.parse_document(sample_kml)
    assert doc.name == 'Test'
    assert len(doc.placemarks) == 4
    assert len(doc.subfolders) == 1
    assert doc.subfolders[0].name == 'Subfolder'
    assert len(doc.subfolders[0].placemarks) == 1
    assert doc.placemarks[0] == sample_linestring_placemark
    assert doc.placemarks[1] == sample_polygon_placemark
    assert isinstance(doc.placemarks[2], high_level.UnknownPlacemark) and doc.placemarks[2].raw_placemark.name == 'Non-kropyva kml'
    assert doc.placemarks[3] == sample_text_placemark
    assert doc.subfolders[0].placemarks[0] == sample_point_placemark


@dataclass
class MockKMLExtractor(GeometryExtractor):
    non_kropyva_placemarks: list[KMLElement] = field(default_factory=list)
    def extract_object(self, obj: KMLElement, context: ExtractorContext | None = None):
        if isinstance(obj, KMLElement):
            self.non_kropyva_placemarks.append(obj)
        else:
            raise ValueError(f'unexpected object type: {type(obj)}')
          
    def extract_file(self, file: io.BufferedReader, context: ExtractorContext | None = None):
        raise NotImplementedError('MockKMLExtractor does not support extract_file')
      
    def requires_password(self):
        return False

def test_tactics_extractor(sample_kme):
    Config().add_default_sidc('')
    kml_extractor = MockKMLExtractor()
    extractor = TacticsExtractor(embedded_kml_extractor=kml_extractor)

    context = ExtractorContext(password='Q1111')
    geometries = extractor.extract_file(sample_kme, context).get_all_geometries()

    assert len(geometries) == 4
    assert geometries[0] == Line(
        name='Назва',
        coordinates=[[35.0, 47.0], [35.005, 47.005]],
        outline_color='#ff0000',
        sidc='10066610001100000000',
    )
    assert geometries[1] == Polygon(
        name='Назва',
        coordinates=[[[35.0, 47.0], [35.005, 47.005], [35.0100, 47.0025], [35.0, 47.0]]],
        outline_color='#ff0000',
        fill_color='#0000ff',
        fill_opacity='1.0',
        sidc='10062510001512030000',
    )
    assert geometries[2] == Point(
        name='Біліна Етанол',
        coordinates=[35.7, 47.4],
        outline_color='#ffa500',
        sidc='10012500001313000000',
        observation_datetime='2024-12-19T15:50:30',
    )
    assert geometries[3] == Point(
        name='Назва',
        coordinates=[35.0, 47.0],
        outline_color='#ff0000',
        sidc='10031000141205000000',
        observation_datetime='2024-12-25T10:36:29',
    )

    assert len(kml_extractor.non_kropyva_placemarks) == 1
    assert kml_extractor.non_kropyva_placemarks[0].name.text == 'Non-kropyva kml'

def test_wrong_kme_password(sample_kme):
    extractor = TacticsExtractor()
    with pytest.raises(InvalidPasswordError):
        extractor.extract_file(sample_kme, context=ExtractorContext(password='WRONG_PASSWORD'))
          