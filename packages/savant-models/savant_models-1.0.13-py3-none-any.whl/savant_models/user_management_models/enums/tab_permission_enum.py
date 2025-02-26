from enum import StrEnum


class TabPermissionEnum(StrEnum):
    EVERYTHING = "everything"
    TEAMS = "teams"
    PERSONAL = "personal"
    NOTHING = "nothing"
