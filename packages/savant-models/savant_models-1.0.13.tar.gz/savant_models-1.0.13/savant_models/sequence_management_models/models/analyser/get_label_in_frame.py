from typing import Optional

from pydantic import BaseModel

from savant_models.sequence_management_models.models.frame.frame_label import FrameLabel
from savant_models.sequence_management_models.models.sequence.sequence_frontend import SequenceFrontend


class GetLabelInFrame(BaseModel):
    label: Optional[FrameLabel] = None
    frame_index: int
    sequence: SequenceFrontend
