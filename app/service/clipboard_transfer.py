from app.infrastructure.fastapi_client import FastAPIClient
from app.service.message_model import MessageModel


class ClipboardTransfer:
    def __init__(self, clipboard):
        self.__local_messages: list[MessageModel] = []
        self.__net_client = FastAPIClient(self.__local_messages)
        self.__clipboard = clipboard

    def get_remote_messages(self) -> list[MessageModel]:
        return self.__local_messages

    def get_local_messages(self) -> list[MessageModel]:
        return self.__clipboard.get_messages()

    def post_messages(self, messages: list[MessageModel]):
        self.__net_client.send_messages(messages)

    def paste_messages(self, messages: list[MessageModel]):
        self.__clipboard.paste_messages(messages)

    def get_ips(self) -> list[str]:
        pass
