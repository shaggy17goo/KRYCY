import json
import subprocess

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Alert(BaseModel):
    name: str
    content: str


class Firewall(BaseModel):
    list_of_ip: str


@app.put("/alert")
def print_log(alert: Alert):
    print("ALERT\n " +
          "name: " + alert.name + "content: " + alert.content)


@app.put("/firewall")
def print_log(firewall: Firewall):
    list_of_ip = json.loads(firewall.list_of_ip)
    for ip in list_of_ip:
        # zeby nic sie nie popsulo
        result = subprocess.getoutput(f"echo 'iptables -A INPUT -s {ip} -j DROP'")
        print(result)


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True, access_log=False)
