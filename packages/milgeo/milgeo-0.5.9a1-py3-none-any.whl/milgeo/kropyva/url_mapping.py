import io
import csv
from dataclasses import dataclass
from pathlib import Path
import re
import importlib.resources
from importlib.resources.abc import Traversable
from milgeo.utils.sidc_utlis import set_sidc_identity

DEFAULT_MAPPING_FILE = __file__.replace('url_mapping.py', 'mapping.csv')

@dataclass
class UrlToSidcMappingEntry:
    url_pattern: re.Pattern
    sidc: str
    identity_from_color: bool
    staff_comments: str | None
    reverse_points: bool

class UrlToSidcMapping:
    def __init__(self, mapping_entries: list[UrlToSidcMappingEntry] | None = None):
        self.mapping = mapping_entries or self.load_mapping(self._default_mapping_path()) # type: ignore because Traversable similar to Path but not Path

    def _default_mapping_path(self) -> Traversable:
        assert __package__ is not None
        return importlib.resources.files(__package__).joinpath('mapping.csv')

    def load_mapping(self, mapping_file: str | Path) -> list[UrlToSidcMappingEntry]:
        try:
            with open(mapping_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, fieldnames=['url_pattern', 'sidc', 'identity_from_color', 'staff_comments', 'reverse_points'])
                return [UrlToSidcMappingEntry(
                    url_pattern=re.compile(row['url_pattern']),
                    sidc=row['sidc'],
                    identity_from_color=row['identity_from_color'] == '1',
                    staff_comments=row['staff_comments'] or None,
                    reverse_points=row['reverse_points'] == '1'
                ) for row in reader]
        except Exception as e:
            print(f"Error loading url to sidc mapping: {e}")
            return []

    def find_entry(self, url: str) -> UrlToSidcMappingEntry | None:
        url = self._prepare_url(url)
        for entry in self.mapping:
            if entry.url_pattern.fullmatch(url):
                return entry
        return None

    def map_url(self, url: str, identity_from_color: str | None, base_sidc: str | None = None) -> str | None:
        url = self._prepare_url(url)

        for entry in self.mapping:
            if not entry.url_pattern.fullmatch(url):
                continue

            if base_sidc is None:
                if url.isdigit():
                    base_sidc = url.ljust(20, '0')
                else:
                    base_sidc = '10010000000000000000'

            matched = entry.sidc
            resulting_sidc = ''.join(matched[i]
                                     if matched[i] != '.' else base_sidc[i]
                                     for i in range(20))
            if entry.identity_from_color and identity_from_color:
                resulting_sidc = set_sidc_identity(resulting_sidc, identity_from_color)
            return resulting_sidc
        
        if all(char.isdigit() for char in url):
            return url.ljust(20, '0')
        return None

    @classmethod
    def _unwrap_kropyva_url(cls, url: str) -> str:
        if url.startswith('url(') and url.endswith(')'):
            url = url[4:-1]
        if url.startswith('!'):
            url = url[1:]
        return url
    
    @classmethod
    def _prepare_url(cls, url: str) -> str:
        url = cls._unwrap_kropyva_url(url)
        if url.isdigit():
            url = url.ljust(20, '0')
        return url

