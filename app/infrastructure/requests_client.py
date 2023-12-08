from requests import post

from app.service.message_model import MessageModel


class RequestsClient:
    @staticmethod
    def send_messages(messages: list[MessageModel]):
        headers = {
            "Content-Type": "application/json",
        }

        data = {"messages": [message.__dict__ for message in messages]}
       #  data = {
       #      "messages": [
       #          {
       #              "sender": {"ip": message.sender.ip, "alias": message.sender.alias},
       #              "receiver": {"ip": message.receiver.ip, "alias": message.receiver.alias},
       #              "content": message.content
       #          }
       #          for message in messages
       #      ]
       #  }

        response = post(f"http://{messages[0].receiver}:8000/messages", headers=headers, json=data)
