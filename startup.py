import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from app.infrastructure.clipboard import Clipboard
from app.infrastructure.requests_client import RequestsClient
from app.service.clipboard_transfer import ClipboardTransfer
from app.service.message_model import MessageModel
from app.utils import get_local_ip, run_with_admin_rights, run_powershell_script

application = FastAPI()
clipboard_transfer = ClipboardTransfer(RequestsClient(), Clipboard())
PORT = 8000


class MessageList(BaseModel):
    messages: list[MessageModel]


@application.post("/messages")
def post_messages(messages: MessageList):
    clipboard_transfer.remote_messages.extend(messages.messages)
    return {'Ok': 'successful'}


if __name__ == "__main__":
    run_with_admin_rights()
    run_powershell_script(r'app/other/enable_ping.PS1')
    uvicorn.run(application, host=get_local_ip(), port=PORT)
