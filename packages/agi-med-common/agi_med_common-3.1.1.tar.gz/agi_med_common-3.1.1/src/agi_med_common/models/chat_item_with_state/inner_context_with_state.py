from ..chat_item import InnerContextItem
from pydantic import Field

from . import ReplicaWithState


class InnerContextWithState(InnerContextItem):
    replicas: list[ReplicaWithState] = Field(alias="Replicas")
