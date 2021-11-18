import base64

import click
import requests

url="http://127.0.0.1:8000/"

@click.command()
def get_pcap_list():
    result = requests.get(url+"getPcapList")
    print(result.json())


@click.command()
@click.option('--name', '-n', default="", help='File to transfer')
def get_pcap(name):
    result = requests.get(url + "getPcap?name=" + name)
    file = open(name, 'wb')
    file.write(base64.b64decode(result.content))

