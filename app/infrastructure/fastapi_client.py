from app.service.message_model import MessageModel
from startup import app


class FastAPIClient:
    def __init__(self, messages: list[MessageModel]):
        self.__messages = messages

    @app.post("/post_message")
    def post_messages(self, message):
        # TODO: parse request body into MessageModel
        # TODO: add messages to ClipboardTransfer
        pass

    def send_messages(self, messages: list[MessageModel]):
        # use requests
        pass