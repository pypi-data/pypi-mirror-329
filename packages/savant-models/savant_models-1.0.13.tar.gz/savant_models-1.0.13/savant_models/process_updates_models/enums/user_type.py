from enum import StrEnum


class UserType(StrEnum):
    
    IM = "internal manager"
    EM = "external manager"
    IA = "internal annotator"
    EA = "external annotator"
    ME = "ml engineer"
    RES = "researcher"
    SUPER = "superuser"

