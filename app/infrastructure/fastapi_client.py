from fastapi import APIRouter
from pydantic import BaseModel
from startup import clipboard_transfer
from app.service.message_model import MessageModel

router = APIRouter()


class MessageList(BaseModel):
    messages: list[MessageModel]


@router.post("/post_messages")
def post_messages(messages: MessageList):
    print(messages)
    clipboard_transfer.remote_messages.extend(messages.messages)
    print(*clipboard_transfer.remote_messages)
    return {'Ok': 'successful'}


def configure_endpoints(app):
    app.include_router(router)
