from datetime import datetime

from pydantic import Field, field_validator, field_serializer

from .. import _Base

_TIME_FORMAT: str = "%Y-%m-%d-%H-%M-%S"
_EXAMPLE_DATETIME: datetime = datetime(1970, 1, 1, 0, 0, 0)


class ReplicaItem(_Base):
    body: str = Field("", alias="Body", examples=["Привет"])
    role: bool = Field(False, alias="Role", description="True = ai, False = client", examples=[False])
    date_time: datetime = Field(
        _EXAMPLE_DATETIME,
        alias="DateTime",
        examples=[_EXAMPLE_DATETIME.strftime(_TIME_FORMAT)],
        description=f"Format: {_TIME_FORMAT}",
    )
    previous_score: float | None = Field(None, alias="PreviousScore", exclude=True, deprecated=True)

    @field_validator("date_time", mode="before")
    @classmethod
    def convert_date_time(cls, timestamp: str | datetime) -> datetime:
        if isinstance(timestamp, datetime):
            return timestamp
        return datetime.strptime(timestamp, _TIME_FORMAT)

    @field_serializer("date_time")
    def serialize_date_time(self, timestamp: datetime) -> str:
        return timestamp.strftime(_TIME_FORMAT)
