from ..chat_item import ReplicaItem
from pydantic import Field

from ..enums import StatesEnum


class ReplicaWithState(ReplicaItem):
    state: StatesEnum | None = Field(None, alias="State")
