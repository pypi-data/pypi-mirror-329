from enum import StrEnum


class Environment(StrEnum):
    TESTING = "testing"
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
