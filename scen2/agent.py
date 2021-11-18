import genericpath
import os
import re
import subprocess

import pyshark
import uvicorn
from fastapi import FastAPI, responses
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()


class pysharkParam(BaseModel):
    interface: str
    bpf_filter: str
    time: int


pcaps = "/var/log/krycy/pcaps/"
logs = "/var/log/krycy/logs/"


if __name__ == "__main__":
    uvicorn.run("agent:app", port=8000, reload=True, access_log=False)


@app.get("/getIfconfig")
def get_ifconfig():
    return subprocess.check_output(["ifconfig"])


@app.put("/sniffing")
def sniffing(param: pysharkParam):
    Path(pcaps).mkdir(parents=True, exist_ok=True)
    logs = os.listdir(pcaps)
    if len(logs) == 0:
        logname = "pyshark.1.pcap"
    else:
        logs = sorted(logs, key=lambda x: (len(x), x))
        lastindex = re.search('\d+', logs[-1]).group(0)
        logname = "pyshark." + str(int(lastindex) + 1) + ".pcap"
    print(pcaps + logname)
    cap = pyshark.LiveCapture(interface=param.interface, bpf_filter=param.bpf_filter, output_file=pcaps + logname)
    cap.sniff(timeout=param.time)

    return responses.FileResponse(pcaps + logname)


@app.get("/getPcapList")
def get_pcap_list():
    Path(pcaps).mkdir(parents=True, exist_ok=True)
    return os.listdir(pcaps)


@app.get("/getPcap")
def get_pcap(name):
    Path(pcaps).mkdir(parents=True, exist_ok=True)
    if os.path.isfile(pcaps + name):
        return responses.FileResponse(pcaps + name)
    return "File doesn't exits"

@app.get("/getLogList")
def get_log_list():
    Path(logs).mkdir(parents=True, exist_ok=True)
    return os.listdir(logs)


@app.get("/getLog")
def get_log(name):
    Path(logs).mkdir(parents=True, exist_ok=True)
    if os.path.isfile(logs+name):
        return responses.FileResponse(logs + name)
    return "File doesn't exits"


@app.get("/command")
def exec_command(command):
    result = subprocess.getoutput(command)
    return result
