from pydantic import ConfigDict

from savant_models.sequence_management_models.enums.to_review_tags_enum import ToReviewTagsEnum
from savant_models.sequence_management_models.models.tags.tag import Tag


class ToReviewTag(Tag):
    """Whole annotation information in the database."""
    label: ToReviewTagsEnum

    model_config = ConfigDict(populate_by_name=True)
