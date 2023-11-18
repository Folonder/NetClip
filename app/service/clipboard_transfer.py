from app.service.message_model import MessageModel
from copy import deepcopy
from app.infrastructure.clipboard import Clipboard
from app.infrastructure.requests_client import RequestsClient


class ClipboardTransfer:
    def __init__(self):
        self.remote_messages: list[MessageModel] = []

    def get_remote_messages(self) -> list[MessageModel]:
        return deepcopy(self.remote_messages)

    def get_local_messages(self) -> list[MessageModel]:
        return Clipboard.get_messages()

    def post_messages(self, messages: list[MessageModel]):
        RequestsClient.send_messages(messages)

    def paste_messages(self, messages: list[MessageModel]):
        Clipboard.paste_messages(messages)
