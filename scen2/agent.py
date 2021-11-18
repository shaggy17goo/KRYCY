import os
import re
import subprocess
import getpass
import pyshark
import nest_asyncio

from fastapi import FastAPI
from pydantic import BaseModel

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
    cap = pyshark.LiveCapture(interface=param.interface, bpf_filter=param.bpf_filter, output_file=pcaplogs + logname)
    cap.sniff(timeout=param.time)
    return cap


@app.get("/getPcapList")
def get_pcap_list():
    return os.listdir(pcaplogs)


@app.get("/getPcap")
async def get_pcap_list(name):
    cap = pyshark.FileCapture(pcaplogs + name)
    return cap
