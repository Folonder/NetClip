from app.infrastructure.fastapi_client import FastAPIClient
from app.service.message_model import MessageModel
from app.infrastructure.clipboard import Clipboard
from app.infrastructure.requests_client import RequestsClient


class ClipboardTransfer:
    def __init__(self):
        self.__local_messages: list[MessageModel] = []
        self.__receive_client = FastAPIClient(self.__local_messages)
        self.__send_client = RequestsClient()
        self.__clipboard = Clipboard()

    def get_remote_messages(self) -> list[MessageModel]:
        return self.__local_messages

    def get_local_messages(self) -> list[MessageModel]:
        return self.__clipboard.get_messages()

    def post_messages(self, messages: list[MessageModel]):
        self.__send_client.send_messages(messages)

    def paste_messages(self, messages: list[MessageModel]):
        self.__clipboard.paste_messages(messages)

    def get_ips(self) -> list[str]:
        pass
