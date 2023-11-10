from app.service.message_model import MessageModel
import requests


class RequestsClient:
    def send_messages(self, messages: list[MessageModel]):
        url = "http://local/post_messages"

        headers = {
            "Content-Type": "application/json",
        }

        data = {"messages": [message.__dict__ for message in messages]}

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    @staticmethod
    def get_available_port():
        i = 8000
        try:
            while i < 9000:
                response = requests.get(f"http://localhost:{i}/get-port")
                i += 1
        except Exception as ex:
            return i