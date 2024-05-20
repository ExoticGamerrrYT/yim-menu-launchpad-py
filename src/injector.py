import psutil
from pyinjector import inject

PROCESS_NAME = "GTA5.exe"


def find_process_id(process_name):
    """Find the first process with the given name and return its PID."""
    for proc in psutil.process_iter(["name", "pid"]):
        if proc.info["name"] == process_name:
            return proc.info["pid"]
    return None


def inject_dll(pID, dll_path):
    inject(pID, dll_path)  # Uses pyinjector
