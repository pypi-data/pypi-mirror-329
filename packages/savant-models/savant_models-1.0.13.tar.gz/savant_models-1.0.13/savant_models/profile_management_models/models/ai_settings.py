from typing import Optional
from pydantic import ConfigDict, model_validator


from savant_models.utils.base import BaseModel
from savant_models.sequence_management_models.enums.ml_action_enum import MLActionEnum
from savant_models.profile_management_models.enums.ml_model_enum import MLModelEnum


class AISettings(BaseModel):
    action: MLActionEnum
    ml_model: MLModelEnum
    enabled: bool
    is_default: Optional[bool] = False

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def check_card_number_omitted(self):
        if (
            self.action == MLActionEnum.STEREO_MAP
            and self.ml_model != MLModelEnum.UNIMATCH
        ):
            raise ValueError(
                f"Model must be {MLModelEnum.UNIMATCH} for {MLActionEnum.STEREO_MAP} action"
            )
        elif (self.ml_model == MLModelEnum.UNIMATCH) and self.is_default:
            raise ValueError(f"Default model cannot be {MLModelEnum.UNIMATCH}")
        return self
