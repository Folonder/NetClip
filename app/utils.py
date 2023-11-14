import socket
import ctypes
import subprocess
import sys


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


def run_with_admin_rights():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "startup.py", None, 1)
            exit()
    except AttributeError:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "startup.py", None, 1)
        exit()


def run_powershell_script(path):
    try:
        return subprocess.run(' '.join(['powershell.exe', '-File', path]), capture_output=True, text=True, check=True, encoding='cp866')
    except subprocess.CalledProcessError as e:
        print("Error running PowerShell script:", e)
        print("PowerShell Script Error Output:")
        print(e.stderr)