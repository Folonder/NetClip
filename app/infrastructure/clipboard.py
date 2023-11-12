from time import sleep
from app.service.message_model import MessageModel
from pyperclip import copy

from subprocess import run
from re import findall, DOTALL


class Clipboard:
    def __init__(self):
        pass

    def paste_messages(self, messages: list[MessageModel]):
        for message in messages:
            copy(message.data)
            sleep(0.25)

    def get_messages(self) -> list[MessageModel]:
        command = "app/other/SharpClipHistory.exe"

        result = run(command, capture_output=True, text=True, encoding='cp866')
        pattern = r'\[\+\] (.*?)(?=\[\+\]|$)'
        matches = findall(pattern, result.stdout, DOTALL)
        matches.pop(0)
        matches.pop(0)
        output_list = []

        for match in matches:
            match = match[21::].strip('\n')
            output_list.append(MessageModel(None, None, match))

        return output_list
