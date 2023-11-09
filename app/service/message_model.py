from dataclasses import dataclass


@dataclass
class MessageModel:
    sender: str
    receiver: str
    data: str
