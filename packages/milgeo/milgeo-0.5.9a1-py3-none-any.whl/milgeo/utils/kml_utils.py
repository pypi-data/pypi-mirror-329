"""Utility functions for working with KML/KME files."""

from typing import Any
from lxml.etree import _Element as KMLElement


def strip_tag_namespace(element: KMLElement | str) -> str:
    """Remove the XML namespace from a KML tag.
    
    Args:
        element: Either a KMLElement object or a tag string
        
    Returns:
        The tag name without namespace
        
    Examples:
        >>> strip_tag_namespace("{http://www.opengis.net/kml/2.2}Placemark")
        'Placemark'
        >>> strip_tag_namespace(kml_element)  # where element.tag is "{http://earth.google.com/kml/2.1}Document"
        'Document'
    """
    if isinstance(element, KMLElement):
        tag = element.tag
    else:
        tag = element
    return tag.split('}')[-1] 

def deepgetattr(obj, path: str, default = None) -> Any:
    try:
        for attr in path.split('.'):
            obj = getattr(obj, attr)
        return obj
    except AttributeError:
        return default
    
