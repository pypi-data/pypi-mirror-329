from datetime import datetime
from typing import Any

from pydantic import Field

from .. import _Base
from ..enums import StateEnum, ActionEnum

_DATETIME_FORMAT: str = "%Y-%m-%d-%H-%M-%S"
_EXAMPLE_DATETIME: str = datetime(1970, 1, 1, 0, 0, 0).strftime(_DATETIME_FORMAT)


class ReplicaItem(_Base):
    body: str = Field("", alias="Body", examples=["Привет"])
    role: bool = Field(False, alias="Role", description="True = ai, False = client", examples=[False])
    date_time: str = Field(
        _EXAMPLE_DATETIME,
        alias="DateTime",
        examples=[_EXAMPLE_DATETIME],
        description=f"Format: {_DATETIME_FORMAT}",
    )
    state: StateEnum = Field(
        StateEnum.EMPTY, alias="State", description="chat manager fsm state", examples=[StateEnum.COLLECTION]
    )
    action: ActionEnum = Field(
        ActionEnum.START, alias="Action", description="chat manager fsm action", examples=[ActionEnum.DIAGNOSIS]
    )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    @staticmethod
    def DATETIME_FORMAT() -> str:
        return _DATETIME_FORMAT


class ReplicaItemPair(_Base):
    user_replica: ReplicaItem = Field(alias="UserReplica")
    model_replica: ReplicaItem = Field(alias="ModelReplica")
