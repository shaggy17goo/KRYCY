import os
import re
import subprocess

import pyshark
import uvicorn
from fastapi import FastAPI, responses
from pydantic import BaseModel

app = FastAPI()


class pysharkParam(BaseModel):
    interface: str
    bpf_filter: str
    time: int


pcaplogs = "/var/log/pyshark/"

if __name__ == "__main__":
    uvicorn.run("agent:app", port=8000, reload=True, access_log=False)


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

    return responses.FileResponse(pcaplogs + logname)


@app.get("/getPcapList")
def get_pcap_list():
    return os.listdir(pcaplogs)


@app.get("/getPcap")
def get_pcap_list(name):
    return responses.FileResponse(pcaplogs + name)


