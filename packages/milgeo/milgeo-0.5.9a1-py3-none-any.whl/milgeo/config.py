from typing import List
from text_to_sidc.austrian import PatternDict, UnitDesignator


class Config:
    unit_designator = None
    custom_patterns = []
    default_sidc = None
    sidc_from_comments = False

    @classmethod
    def get_unit_designator(cls):
        if cls.unit_designator is None:
            cls.unit_designator = UnitDesignator()
            cls._apply_all_configurations()
        return cls.unit_designator

    @classmethod
    def add_custom_patterns(cls, patterns: List[PatternDict]):
        cls._validate_patterns(patterns)
        cls.custom_patterns.extend(patterns)
        if cls.unit_designator:
            cls._apply_custom_patterns()

    @classmethod
    def add_default_sidc(cls, default_sidc: str):
        cls.default_sidc = default_sidc
        if cls.unit_designator:
            cls._apply_default_sidc()

    @classmethod
    def set_sidc_from_comments(cls, sidc_from_comments: bool):
        cls.sidc_from_comments = sidc_from_comments

    @classmethod
    def _apply_all_configurations(cls):
        cls._apply_custom_patterns()
        cls._apply_default_sidc()

    @classmethod
    def _apply_custom_patterns(cls):
        if cls.custom_patterns:
            cls.unit_designator.import_custom_patterns(cls.custom_patterns)

    @classmethod
    def _apply_default_sidc(cls):
        if cls.default_sidc:
            cls.unit_designator.set_default_sidc(cls.default_sidc)

    @staticmethod
    def _validate_patterns(patterns: List[PatternDict]):
        for pattern_dict in patterns:
            if not all(k in pattern_dict for k in ["sidc", "list_of_patterns"]) or \
                    not isinstance(pattern_dict["list_of_patterns"], list):
                raise ValueError("Each pattern must have 'sidc' and 'list_of_patterns' (list of strings).")
