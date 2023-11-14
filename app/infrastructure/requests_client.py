from app.service.message_model import MessageModel
import requests


class RequestsClient:
    def send_messages(self, messages: list[MessageModel]):
        url = f"http://{messages[0].receiver}:8000/messages"

        headers = {
            "Content-Type": "application/json",
        }

        data = {"messages": [message.__dict__ for message in messages]}

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
