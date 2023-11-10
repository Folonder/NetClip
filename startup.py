from fastapi import FastAPI
from pydantic import BaseModel

from app.infrastructure.clipboard import Clipboard
from app.infrastructure.requests_client import RequestsClient
from app.service.clipboard_transfer import ClipboardTransfer
from app.service.message_model import MessageModel

app = FastAPI()
clipboard_transfer = ClipboardTransfer(RequestsClient(), Clipboard())


class MessageList(BaseModel):
    messages: list[MessageModel]


@app.post("/post-messages")
def post_messages(messages: MessageList):
    print(messages)
    clipboard_transfer.remote_messages.extend(messages.messages)
    return {'Ok': 'successful'}
