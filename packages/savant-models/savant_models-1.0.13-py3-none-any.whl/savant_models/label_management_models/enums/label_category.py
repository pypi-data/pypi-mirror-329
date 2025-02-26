from enum import StrEnum


class LabelCategory(StrEnum):
    STEP = "step"
    PHASE = "phase"
    ANATOMY = "anatomy"
    TOOL = "tool"
    TOOL_PARTS = "tool parts"
    ACTIONS = "actions"
    OBSERVATIONS = "observations"
    COMPLICATIONS = "complications"
    EVENTS = "events"
    ERRORS = "errors"
    OBJECTIVE = "objective"
    TIMESTAMP = "timestamp"
    OTHERS = "others"
