from ..chat_item import ChatItem
from pydantic import Field

from . import InnerContextWithState


class ChatItemWithState(ChatItem):
    inner_context: InnerContextWithState = Field(alias="InnerContext")
