import base64
import sys
import threading

from PyQt5.QtWidgets import QApplication
from fastapi import FastAPI
from uvicorn import run

from app.service.clipboard_transfer import ClipboardTransfer
from app.service.message_model import MessageList, MessageModel
from app.utils import get_local_ip, run_with_admin_rights, run_powershell_script
from app.view.view import View

application = FastAPI()
clipboard_transfer = ClipboardTransfer()



def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def run_server():
    run(application, host=get_local_ip(), port=8000)


def run_view():
    app = QApplication(sys.argv)
    ex = View(clipboard_transfer)
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    thread1 = threading.Thread(target=run_server)
    thread2 = threading.Thread(target=run_view)
    run_with_admin_rights("startup.py")
    run_powershell_script(r'app/other/enable_ping.PS1')
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
