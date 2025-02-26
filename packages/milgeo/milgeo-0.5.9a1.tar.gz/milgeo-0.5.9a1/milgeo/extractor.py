from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from milgeo.geometry import GeometriesList, Geometry


class ExtractionError(Exception):
    """Base class for extraction errors."""
    pass

class PasswordRequiredError(ExtractionError):
    """Raised when a password is required but not provided"""
    pass

class InvalidPasswordError(ExtractionError):
    """Raised when a password is provided but is incorrect"""
    pass

class UnsupportedFileFormatError(ExtractionError):
    """Raised when a file format is not supported"""
    pass

@dataclass
class ExtractorContext:
    """Shared context for extraction operations"""
    password: Optional[str] = None

    # Could add more context like:
    # - coordinate system
    # - validation flags
    # - logging configuration
    # - etc.

class GeometryExtractor(ABC):
    """Base class for geometry extractors"""

    # @abstractmethod
    # def supports_format(self, file) -> bool:
    #     """Check if this extractor can handle the given file format"""
    #     pass

    @abstractmethod
    def requires_password(self, file) -> bool:
        """Check if the file requires a password for extraction"""
        pass

    @abstractmethod
    def extract_file(self, file, context: ExtractorContext | None = None) -> GeometriesList:
        """Extract all geometries from a file"""
        pass

    @abstractmethod
    def extract_object(self, obj, context: ExtractorContext | None = None) -> Optional[Geometry]:
        """Extract geometry from a single object, if possible"""
        pass