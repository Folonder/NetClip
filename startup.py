import threading

from fastapi import FastAPI
from uvicorn import run

from app.service.clipboard_transfer import ClipboardTransfer
from app.service.message_model import MessageList
from app.utils import get_local_ip, run_with_admin_rights, run_powershell_script

application = FastAPI()
clipboard_transfer = ClipboardTransfer()


@application.post("/messages")
def post_messages(messages: MessageList):
    clipboard_transfer.remote_messages.extend(messages.messages)
    return {'Ok': 'successful'}


def run_server():
    run(application, host=get_local_ip(), port=8000)


def run_input():
    for i in range(100):
        print("lol")


if __name__ == "__main__":
    thread1 = threading.Thread(target=run_server)
    thread2 = threading.Thread(target=run_input)
    run_with_admin_rights("startup.py")
    run_powershell_script(r'app/other/enable_ping.PS1')
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

