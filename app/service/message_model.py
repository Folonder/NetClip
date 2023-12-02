from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class MessageModel:
    sender: str
    receiver: str
    content: bytes
    content_type: str

@dataclass
class NetMessageModel:
    sender: str
    receiver: str
    content: str
    content_type: str

class MessageList(BaseModel):
    messages: list[MessageModel]


class NetMessageList(BaseModel):
    messages: list[NetMessageModel]
