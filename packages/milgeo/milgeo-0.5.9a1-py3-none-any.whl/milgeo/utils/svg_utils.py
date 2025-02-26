from dataclasses import dataclass
from typing import Iterable

import svgpathtools as svg
from pyproj import Transformer

from milgeo.utils.coords import CoordPair, WGSCoords


SVG_COORD_SCALE = 1000

wgs84_to_mercator = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
mercator_to_wgs84 = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

class SVGCoords(CoordPair):
    '''Separate class for SVG coordinates (in pixels)'''
    pass


@dataclass
class SVGPathPoint:
    coords: SVGCoords
    is_virtual: bool = False

@dataclass
class LatLonBox:
    west: float
    east: float
    north: float
    south: float

    @property
    def width(self) -> float:
        return self.east - self.west
    
    @property
    def height(self) -> float:
        return self.north - self.south


def _map_val(val, old_min, old_max, new_min, new_max):
    '''
    >>> map_val(1, 1, 4, 0, 9) # start
    0.0
    >>> map_val(4, 1, 4, 0, 9) # end
    9.0
    >>> map_val(2, 1, 4, 0, 9) # one third
    3.0
    >>> map_val(2, 1, 4, 9, 0) # reverse range
    6.0
    >>> map_val(0, 1, 4, 0, 9) # below min
    -3.0
    >>> map_val(6, 1, 4, 0, 9) # above max
    15.0
    '''
    if old_min == old_max:
        return new_min if val <= old_min else new_max
    return (val - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

def _complex_to_svgcoords(complex: complex) -> SVGCoords:
    return SVGCoords(x=complex.real, y=complex.imag)

def _render_svg_path(path: svg.Path, curve_subpoints: int = 0) -> list[SVGPathPoint]:
    points = [SVGPathPoint(coords=_complex_to_svgcoords(path[0][0]), is_virtual=False)]
    if path.iscontinuous() and path.isclosed() and isinstance(path[-1], svg.Line):
        segments = path[:-1] # last segment is added by the library and just joins the first point with the last one
    else:
        segments = path
    for segment in segments:
        if curve_subpoints > 0 and isinstance(segment, svg.CubicBezier):
            ts = [(t + 1) / curve_subpoints for t in range(curve_subpoints)]
            new_points = segment.points(ts)
            points.extend(SVGPathPoint(coords=_complex_to_svgcoords(point), is_virtual=True) for point in new_points[:-1])
            points.append(SVGPathPoint(coords=_complex_to_svgcoords(new_points[-1]), is_virtual=False)) # last point is not virtual
        else:
            point = segment.point(1)
            points.append(SVGPathPoint(coords=_complex_to_svgcoords(point), is_virtual=False))
    return points

def svg_path_to_wgs(path: svg.Path, region: LatLonBox, curve_subpoints: int = 0, precision: int = 6, max_svg_x: float | None = None, max_svg_y: float | None = None) -> tuple[list[WGSCoords], bool]:
    cyclic = path.iscontinuous() and path.isclosed()
    all_points = _render_svg_path(path, curve_subpoints)
    real_points = [p.coords for p in all_points if not p.is_virtual]

    min_x = min(p.x for p in real_points)
    max_x = max_svg_x or max(p.x for p in real_points)
    min_y = min(p.y for p in real_points)
    max_y = max_svg_y or max(p.y for p in real_points)
    if abs(min_x) > 1 or abs(min_y) > 1 or abs(max_x - 1000) > 1 or abs(max_y - 1000) > 1:
        print(f'WARNING: x [{min_x},{max_x}], y [{min_y},{max_y}]')

    west_merc, south_merc, east_merc, north_merc = wgs84_to_mercator.transform_bounds(region.west, region.south, region.east, region.north)
    mercator_path = [(
        _map_val(p.coords.x, 0, max_x, west_merc, east_merc),
        _map_val(p.coords.y, 0, max_y, north_merc, south_merc)
    ) for p in all_points]
    
    wgs_path_raw = [mercator_to_wgs84.transform(x, y) for x, y in mercator_path]
    wgs_path = [WGSCoords.of_xy(round(x, precision), round(y, precision)) for x, y in wgs_path_raw]
    return wgs_path, cyclic

def calc_lat_lon_box(coord_pairs: Iterable[WGSCoords], default_dim = 0.00001) -> LatLonBox:
    ''' Gets a lat-lon bounding box for a list of (Y,X) points.
        If the width or the height for the box is 0, it is set to `default_dim`'''

    ys, xs = zip(*(p.yx for p in coord_pairs))
    res = LatLonBox(
        south=min(ys),
        north=max(ys),
        west=min(xs),
        east=max(xs),
    )
    if res.east == res.west:
        res.east += default_dim
    if res.north == res.south:
        res.north += default_dim
    return res

def to_svg_coord_pair(coord_pair: WGSCoords, lat_lon_box: LatLonBox, scale = SVG_COORD_SCALE) -> SVGCoords:
    ''' Transforms a WSG (Y,X) point into relative (X,Y) coords with respect to `lat_lon_box`.
        X goes from 0 at the east boundary to `scale` at the west,
        Y goes from 0 at the north boundary to `scale` at the south'''
        
    y, x = coord_pair.yx
    dx = lat_lon_box.width
    dy = -lat_lon_box.height
    return SVGCoords(x=(x - lat_lon_box.west) / dx * scale, y=(y - lat_lon_box.north) / dy * scale)

def _round_number(num, precision = 6):
    rounded = round(num, precision)
    if rounded == int(rounded):
        return int(rounded)
    return round(rounded, precision)

def _round_complex(num: complex, precision = 6) -> complex:
    return complex(
        _round_number(num.real, precision),
        _round_number(num.imag, precision)
    )

def _svgcoord_to_complex(svg_coord: SVGCoords, precision = 6) -> complex:
    return _round_complex(complex(svg_coord.x, svg_coord.y), precision)

def to_svg_path(points: list[WGSCoords], lat_lon_box: LatLonBox | None = None, closed: bool = False) -> svg.Path:
    lat_lon_box = lat_lon_box or calc_lat_lon_box(points)
    svg_points = [to_svg_coord_pair(x, lat_lon_box) for x in points]
    complex_points = [_svgcoord_to_complex(p) for p in svg_points]
    if closed:
        return svg.polygon(*complex_points)
    return svg.polyline(*complex_points)

def join_paths(paths: Iterable[svg.Path]) -> svg.Path:
    '''Join a list of paths into a single path. If the paths are not continuous, join them with a line.'''
    result = svg.Path()
    for path in paths:
        if len(result) > 0 and result.end != path.start:
            result.append(svg.Line(result.end, path.start))
        result.extend(path)
    return result

def _round_path_segment(segment, precision: int):
    if isinstance(segment, svg.Path):
        return svg.Path(*[_round_path_segment(p, precision) for p in segment])
    elif isinstance(segment, svg.Line) or isinstance(segment, svg.CubicBezier):
        segment.start = _round_complex(segment.start, precision)
        segment.end = _round_complex(segment.end, precision)
        return segment
    return segment

def round_path_points(path: svg.Path, precision: int) -> svg.Path:
    return _round_path_segment(path, precision)
