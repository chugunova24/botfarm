import enum


class EnvironmentEnum(enum.Enum):
    stage = "stage"
    preprod = "preprod"
    prod = "prod"


class DomainEnum(enum.Enum):
    canary = "canary"
    regular = "regular"
