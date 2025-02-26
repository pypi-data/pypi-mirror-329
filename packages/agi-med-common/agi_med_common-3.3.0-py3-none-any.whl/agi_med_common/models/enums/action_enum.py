from enum import StrEnum, auto


class ActionEnum(StrEnum):
    START = auto()

    GREETING = auto()
    MODERATION = auto()
    ANSWER = auto()
    QUESTION = auto()
    CRITICAL = auto()
    MED_TEST_DECRYPTION = auto()

    DIAGNOSIS = auto()
    REPORT = auto()

    FINAL = auto()
