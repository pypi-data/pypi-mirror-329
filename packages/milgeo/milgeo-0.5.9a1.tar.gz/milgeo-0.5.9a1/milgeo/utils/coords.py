from dataclasses import dataclass
from typing import TypeVar


@dataclass(kw_only=True, frozen=True)
class CoordPair:
    x: float
    y: float

    @classmethod
    def of_xy(cls, x: float, y: float):
        return cls(x=x, y=y)
    
    @classmethod
    def of_yx(cls, y: float, x: float):
        return cls(x=x, y=y)
    
    @property
    def xy(self):
        return (self.x, self.y)

    @property
    def yx(self):
        return (self.y, self.x)


class WGSCoords(CoordPair):
    '''
    WGS-84 LatLon/XY coordinates.
    '''
    
    @property
    def lat(self) -> float:
        return self.y
    
    @property
    def lon(self) -> float:
        return self.x
    
    @classmethod
    def of_latlon(cls, lat: float, lon: float):
        return cls(y=lat, x=lon)


'''Generic coordinate pair type variable.'''
_TCoordPair = TypeVar('_TCoordPair', bound=CoordPair)
