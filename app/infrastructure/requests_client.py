import base64

from requests import post

from app.service.message_model import MessageModel


class RequestsClient:
    @staticmethod
    def send_messages(messages: list[MessageModel]):
        # headers = {
        #     "Content-Type": "application/json",
        # }
        headers = {'Content-Type': 'application/json;'}

        data = {"messages": [RequestsClient.to_dict(message) for message in messages]}

        response = post(f"http://{messages[0].receiver}:8000/messages", headers=headers, json=data)

    @staticmethod
    def to_dict(message: MessageModel):
        return {
            "sender": message.sender,
            "receiver": message.receiver,
            "content": message.content.decode('cp866'),
            "content_type": message.content_type
        }