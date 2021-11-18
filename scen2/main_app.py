import click
import requests
from pydantic import BaseModel

url = "http://127.0.0.1:8000/"


class pysharkParam(BaseModel):
    interface: str
    bpf_filter: str
    time: int


@click.command()
def get_ifconfig():
    result = requests.get(url + "getIfconfig")
    print(result.json())


@click.command()
def get_pcap_list():
    result = requests.get(url + "getPcapList")
    print(result.json())


@click.command()
@click.option('--file', '-f', default=[], multiple= True, help='File to transfer')
def get_pcap(file):
    for f in file:
        result = requests.get(url + "getPcap?name=" + f)
        file = open(f, 'wb')
        file.write(result.content)



@click.command()
@click.option('--interface', '-i', default="", help='Interface')
@click.option('--filter', '-f', default="", help='Filter')
@click.option('--time', '-t', default=1, help='Time')
@click.option('--name', '-n', default="", help='Name')
def sniff(interface, filter, time, name):
    param = pysharkParam(interface=interface, bpf_filter=filter, time=time)
    result = requests.put(url + "sniffing", data=param.json())
    file = open(name, 'wb')
    file.write(result.content)

