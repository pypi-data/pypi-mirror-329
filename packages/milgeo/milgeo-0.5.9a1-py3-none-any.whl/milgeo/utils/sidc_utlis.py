from enum import Enum


def set_sidc_identity(sidc: str, identity: str) -> str:
    '''
    Set the identity of the SIDC (the third and fourth characters)
    '''
    assert len(identity) in [1, 2], 'Identity must be a single character or a pair of characters'
    identity = identity.rjust(2, '0')
    return sidc[:2] + identity + sidc[4:]

def get_sidc_identity_from_color(color: str | None) -> str:
    '''
    Get APP-6(D) identity from a color.
    TODO: add more colors
    '''
    match (color or '').lower():
        case 'red' | '#9d2400': return '6'
        case 'green' | '#00ff00': return '4'
        case 'blue' | '#00ffff' | '#0f78ff': return '3'
        case _: return '1'


class SidcAmplifier(Enum):
    UNKNOWN = '00'
    TEAM_CREW = '11'
    SQUAD = '12'
    SECTION = '13'
    PLATOON_DETACHMENT = '14'
    COMPANY_BATTERY_TROOP = '15'
    BATTALION_SQUADRON = '16'
    REGIMENT_GROUP = '17'
    BRIGADE = '18'
    VERSION_EXTENSION_FLAG_1 = '19'
    DIVISION = '21'
    CORPS = '22'
    ARMY = '23'
    ARMY_GROUP_FRONT = '24'
    REGION_THEATRE = '25'
    COMMAND = '26'
    VERSION_EXTENSION_FLAG_2 = '29'

def set_sidc_amplifier(sidc: str, amplifier: SidcAmplifier) -> str:
    return sidc[:8] + amplifier.value + sidc[10:]
