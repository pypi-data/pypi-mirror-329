import enum
from enum import StrEnum
from logging import DEBUG, INFO, WARNING


class EnvironmentType(StrEnum):
    PRODUCTION = "PRODUCTION"
    BETA = "BETA"  # human test
    ALPHA = "ALPHA"  # human test
    TEST = "TEST"  # automatic test
    DEV = "DEV"
    LOCAL = "LOCAL"

    @enum.property
    def is_local(self) -> bool:
        return self == self.LOCAL

    @enum.property
    def is_dev(self) -> bool:
        return self == self.DEV

    @enum.property
    def is_test(self) -> bool:
        return self in (self.BETA, self.ALPHA, self.TEST)

    @enum.property
    def is_production(self) -> bool:
        return not self.is_test and not self.is_dev and not self.is_local

    @enum.property
    def log_level(self) -> int:
        if self.is_production:
            return WARNING
        elif self.is_test:
            return INFO
        else:
            return DEBUG
