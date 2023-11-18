from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class MessageModel:
    sender: str
    receiver: str
    data: str


class MessageList(BaseModel):
    messages: list[MessageModel]