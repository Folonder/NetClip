from app.service.message_model import MessageModel


class ClipboardTransfer:
    def __init__(self, send_client, clipboard):
        self.remote_messages: list[MessageModel] = []
        self.__send_client = send_client
        self.__clipboard = clipboard

    def get_remote_messages(self) -> list[MessageModel]:
        return self.remote_messages

    def get_local_messages(self) -> list[MessageModel]:
        return self.__clipboard.get_messages()

    def post_messages(self, messages: list[MessageModel]):
        self.__send_client.send_messages(messages)

    def paste_messages(self, messages: list[MessageModel]):
        self.__clipboard.paste_messages(messages)

    def get_ips(self) -> list[str]:
        pass
