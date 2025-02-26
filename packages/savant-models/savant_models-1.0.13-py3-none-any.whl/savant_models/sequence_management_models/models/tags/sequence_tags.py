from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.sequence_management_models.models.tags.tag import Tag
from savant_models.sequence_management_models.models.tags.to_annotate_tag import ToAnnotateTag
from savant_models.sequence_management_models.models.tags.to_review_tag import ToReviewTag


class SequenceTags(BaseModel):
    """Whole annotation information in the database."""
    to_review: Optional[List[ToReviewTag]] = []
    to_annotate: Optional[List[ToAnnotateTag]] = []
    profile_sequence: Optional[List[Tag]] = []
    profile_hidden_tag: Optional[List[ProfileTag]] = []

    model_config = ConfigDict(populate_by_name=True)
