from app.service.message_model import MessageModel
import requests


class RequestsClient:
    @staticmethod
    def send_messages(messages: list[MessageModel]):
        url = f"http://{messages[0].receiver}:8000/messages"

        headers = {
            "Content-Type": "application/json",
        }

        data = {"messages": [message.__dict__ for message in messages]}

        response = requests.post(url, headers=headers, json=data)

