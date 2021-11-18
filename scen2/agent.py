import os
import re
import subprocess
import getpass
import time
import pyshark
import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import base64



user = getpass.getuser()
pcaplogs = "/home/" + user + "/pcaplogs/"


app = FastAPI()


class pysharkParam(BaseModel):
    interface: str
    bpf_filter: str
    time: int


@app.get("/getIfconfig")
def get_ifconfig():
    return subprocess.check_output(["ifconfig"])


@app.put("/sniffing")
def sniffing(param: pysharkParam):
    logs = os.listdir(pcaplogs)
    if len(logs) == 0:
        logname = "pyshark.1.pcap"
    else:
        logs = sorted(logs, key=lambda x: (len(x), x))
        lastindex = re.search('\d+', logs[-1]).group(0)
        logname = "pyshark." + str(int(lastindex) + 1) + ".pcap"
    print(pcaplogs + logname)
    cap = pyshark.LiveCapture(interface=param.interface, bpf_filter=param.bpf_filter, output_file=pcaplogs+logname)
    cap.sniff(timeout=param.time)
    with open(pcaplogs + logname, "rb") as f:
        byte = f.read()
    file = base64.b64encode(byte)
    return file


@app.get("/getPcapList")
def get_pcap_list():
    return os.listdir(pcaplogs)


@app.get("/getPcap")
def get_pcap_list(name):
    with open(pcaplogs+name, "rb") as f:
        byte = f.read()
    file = base64.b64encode(byte)
    return file
