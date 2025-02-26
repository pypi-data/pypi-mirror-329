from typing import Union, Dict, Type

from pydantic import BaseModel

from savant_models.profile_management_models.enums.auto_qa.check_level import CheckLevel
from savant_models.profile_management_models.enums.auto_qa.qa_rule_name import QARuleName
from savant_models.profile_management_models.enums.auto_qa.qa_rule_url import QARuleURL
from savant_models.profile_management_models.models.auto_qa.parameters.label_codes import LabelCodes
from savant_models.profile_management_models.models.auto_qa.parameters.label_codes_region import LabelCodesRegion
from savant_models.profile_management_models.models.auto_qa.parameters.label_codes_shape_type_max_count import \
    LabelCodesShapeTypeMaxCount
from savant_models.profile_management_models.models.auto_qa.parameters.label_counts import LabelCounts
from savant_models.profile_management_models.models.auto_qa.parameters.label_subset import LabelSubset
from savant_models.profile_management_models.models.auto_qa.parameters.label_subsets import LabelSubsets
from savant_models.profile_management_models.models.auto_qa.parameters.labels_to_relative_labels import LabelsToRelativeLabels
from savant_models.profile_management_models.models.auto_qa.parameters.length import Length
from savant_models.profile_management_models.models.auto_qa.parameters.shape_coverages import ShapeCoverages
from savant_models.profile_management_models.models.auto_qa.parameters.skeleton_sub_type_count import SkeletonSubTypeCount
from savant_models.profile_management_models.models.auto_qa.parameters.section_label_count import SectionLabelCount


class QARuleConfig:
    parameters_types = Union[
        LabelCodesShapeTypeMaxCount, LabelCodesRegion, SkeletonSubTypeCount, LabelCodes, LabelSubset, LabelSubsets,
        LabelCounts, LabelsToRelativeLabels, Length, ShapeCoverages, SectionLabelCount
    ]

    validation_rules: Dict[QARuleName, Dict[str, Union[QARuleURL, CheckLevel, Type[BaseModel]]]] = {
        QARuleName.KEYPOINT_IN_BOUNDING_BOX: {
            "url": QARuleURL.KEYPOINT_IN_BOUNDING_BOX,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelCodes,
        },
        QARuleName.SHAPE_TYPE_COUNT: {
            "url": QARuleURL.SHAPE_TYPE_COUNT,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelCodesShapeTypeMaxCount,
        },
        QARuleName.SKELETON_SUB_TYPE_COUNT: {
            "url": QARuleURL.SKELETON_SUB_TYPE_COUNT,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": SkeletonSubTypeCount,
        },
        QARuleName.LABEL_COUNT: {
            "url": QARuleURL.LABEL_COUNT,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelCounts,
        },
        QARuleName.SHAPE_COVERAGE: {
            "url": QARuleURL.SHAPE_COVERAGE,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": ShapeCoverages,
        },
        QARuleName.LABEL_IN_REGION: {
            "url": QARuleURL.LABEL_IN_REGION,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelCodesRegion,
        },
        QARuleName.LABEL_RELATIVE_SIZE: {
            "url": QARuleURL.LABEL_RELATIVE_SIZE,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelsToRelativeLabels,
        },
        QARuleName.LABEL_RELATIVE_POSITION: {
            "url": QARuleURL.LABEL_RELATIVE_POSITION,
            "check_level": [CheckLevel.FRAME],
            "parameters_type": LabelsToRelativeLabels,
        },
        QARuleName.LABEL_SUBSET: {
            "url": QARuleURL.LABEL_SUBSET,
            "check_level": [CheckLevel.FRAME, CheckLevel.SEQUENCE],
            "parameters_type": LabelSubset,
        },
        QARuleName.LABEL_MULTIPLE_SUBSETS: {
            "url": QARuleURL.LABEL_MULTIPLE_SUBSETS,
            "check_level": [CheckLevel.FRAME, CheckLevel.SEQUENCE],
            "parameters_type": LabelSubsets,
        },
        QARuleName.PHASE_LENGTH: {
            "url": QARuleURL.PHASE_LENGTH,
            "check_level": [CheckLevel.VIDEO],
            "parameters_type": Length,
        },
        QARuleName.PHASE_LABEL_COUNT: {
            "url": QARuleURL.PHASE_LABEL_COUNT,
            "check_level": [CheckLevel.VIDEO],
            "parameters_type": LabelCounts,
        },
        QARuleName.PHASE_SECTION_LABEL_COUNT: {
            "url": QARuleURL.PHASE_SECTION_LABEL_COUNT,
            "check_level": [CheckLevel.VIDEO],
            "parameters_type": SectionLabelCount,
        },
        QARuleName.PHASE_ORDER: {
            "url": QARuleURL.PHASE_ORDER,
            "check_level": [CheckLevel.VIDEO],
            "parameters_type": LabelCodes,
        }
    }
