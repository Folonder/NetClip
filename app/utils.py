import ctypes
from socket import gethostbyname, gethostname
from subprocess import run, CalledProcessError
from sys import executable


def get_local_ip():
    return gethostbyname(gethostname())


def run_with_admin_rights(filename):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, filename, None, 1)
        exit()


def run_powershell_script(path):
    try:
        return run(['powershell.exe', '-File', path], capture_output=True, text=True, check=True, encoding='cp866')
    except CalledProcessError as e:
        print("Error running PowerShell script:", e)
        print("PowerShell Script Error Output:")
        print(e.stderr)
