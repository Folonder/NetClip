import os
from re import findall, DOTALL
from subprocess import run
from time import sleep

from pyperclip import copy
import win32clipboard
from io import BytesIO
from PIL import Image

from app.service.message_model import MessageModel
from app.utils import get_local_ip


class Clipboard:
    def __init__(self):
        pass

    @staticmethod
    def paste_messages(messages: list[MessageModel]):
        for message in messages:
            if message.content_type == 'text':
                copy(message.content.decode('utf-8'))
            elif message.content_type == 'image':
                img = Image.open(BytesIO(message.content))
                Clipboard.paste_image(img)
            sleep(0.5)

    @staticmethod
    def paste_image(img):
        output = BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        Clipboard.send_to_clipboard(data)

    @staticmethod
    def send_to_clipboard(data):
        clip_type = win32clipboard.CF_DIB
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    @staticmethod
    def get_messages() -> list[MessageModel]:
        result = run("app/other/SharpClipHistory.exe --saveImages", capture_output=True, text=True, encoding='cp866')
        message_model_list = Clipboard.get_messages_in_order(result)
        return message_model_list

    @staticmethod
    def get_messages_in_order(result):
        matches = findall(r'\[\+] (.*?)(?=\[\+]|$)', result.stdout, DOTALL)
        matches = matches[2:]
        message_model_list = []
        for match in matches:
            message_model_list.append(Clipboard.get_message_model(match))
        Clipboard.clear_dir('app/other/images')
        return message_model_list

    @staticmethod
    def get_message_model(match):
        if "SharpClipHistory - Image found and saved in" in match:
            content_type = 'image'
            match = match.strip()
            content_path = match[match.find('in') + 3:-1]  # взять путь к файлу
            img = Image.open(content_path)
            output = BytesIO()
            img.convert("RGB").save(output, "BMP")
            content = output.getvalue()
            output.close()
        else:
            content_type = 'text'
            content = match[21:].strip('\n').encode('utf-8')
        return MessageModel("get_local_ip()", None, content, content_type)

    @staticmethod
    def clear_dir(dir):
        for file in os.scandir(dir):
            os.remove(file)

