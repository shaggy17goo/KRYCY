import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Alert(BaseModel):
    name: str
    content: str


class Firewall(BaseModel):
    action: str


@app.put("/alert")
def print_log(alert: Alert):
    print("ALERT\n " +
          "name: " + alert.name + "content: " + alert.content)


@app.put("/firewall")
def print_log(firewall: Firewall):
    print("FIREWALL\n " +
          "action: " + firewall.action)
    os.system(firewall.action)


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True, access_log=False)


# requests.put('http://127.0.0.1:8000/alert', json={'name': 'WSTWAWAJ KURWAAAA', 'content': 'ATAKUJO NAS'})
# requests.put('http://127.0.0.1:8000/firewall', json={'action': 'iptables --help ; rm * ')
