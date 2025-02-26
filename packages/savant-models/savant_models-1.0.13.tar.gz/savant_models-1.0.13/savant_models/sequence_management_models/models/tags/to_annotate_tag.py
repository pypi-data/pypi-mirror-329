from pydantic import ConfigDict

from savant_models.sequence_management_models.enums.to_annotate_tags_enum import ToAnnotateTagsEnum
from savant_models.sequence_management_models.models.tags.tag import Tag


class ToAnnotateTag(Tag):
    label: ToAnnotateTagsEnum

    model_config = ConfigDict(populate_by_name=True)
