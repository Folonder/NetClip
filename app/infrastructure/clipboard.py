from re import findall, DOTALL
from subprocess import run
from time import sleep

from pyperclip import copy

from app.service.message_model import MessageModel
from app.utils import get_local_ip


class Clipboard:
    def __init__(self):
        pass

    @staticmethod
    def paste_messages(messages: list[MessageModel]):
        for message in messages:
            copy(message.data)
            sleep(0.5)

    @staticmethod
    def get_messages() -> list[MessageModel]:
        result = run("app/other/SharpClipHistory.exe", capture_output=True, text=True, encoding='cp866')
        matches = findall(r'\[\+] (.*?)(?=\[\+]|$)', result.stdout, DOTALL)
        return [MessageModel(get_local_ip(), None, match[20:].strip('\n')) for match in matches[2:]]
