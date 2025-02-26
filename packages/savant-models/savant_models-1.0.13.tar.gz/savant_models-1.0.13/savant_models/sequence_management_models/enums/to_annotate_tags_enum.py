from enum import StrEnum


class ToAnnotateTagsEnum(StrEnum):
    EDGE_CASE = "edge_case"
    UNKNOWN_ANATOMY = "unknown_anatomy"
    UNKNOWN_INSTRUMENT = "unknown_instrument"
    ANNOTATOR_QUERY = "annotator_query"
