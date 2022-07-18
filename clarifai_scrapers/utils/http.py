# SYSTEM IMPORTS
import shlex
import subprocess
import json


def call_curl(curl: str):
    args           = shlex.split(curl)
    process        = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    return json.loads(stdout.decode('utf-8'))