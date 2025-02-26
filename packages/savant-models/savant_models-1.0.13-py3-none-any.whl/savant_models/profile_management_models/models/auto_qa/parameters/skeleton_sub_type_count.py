from typing import Optional

from savant_models.profile_management_models.models.auto_qa.parameters.label_codes import LabelCodes

from savant_models.skeleton_management_models.models.skeleton import Skeleton


class SkeletonSubTypeCount(LabelCodes):
    skeleton: Skeleton
    max_count: int
    sub_type: Optional[str] = None
