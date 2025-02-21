from enum import StrEnum, auto


class StatesEnum(StrEnum):
    """
    Класс для хранения имен состояний.
    """

    BEGIN = auto()
    START = auto()

    IS_CHILD = auto()
    IS_ABSURD = auto()
    CRITICAL = auto()
    WHAT_COMPLAINTS = auto()
    NOT_MEDICAL = auto()

    ERROR_STATE = auto()

    CONSULTATION_TRANSIT = auto()
    NOT_MEDICAL_DOC = auto()
    CONSULTATION = auto()

    INFO_COLLECTION = auto()
    MAKE_DIAGNOSIS = auto()

    SUMMARIZATION = auto()
    MEDICAL_TEST_RECOMMENDATION = auto()

    ANALYSIS_CONSULTATION = auto()
