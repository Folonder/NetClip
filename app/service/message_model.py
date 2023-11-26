from dataclasses import dataclass
from app.service.ip_model  import IpModel
from pydantic import BaseModel


@dataclass
class MessageModel:
    sender: IpModel
    receiver: IpModel
    content: str


class MessageList(BaseModel):
    messages: list[MessageModel]