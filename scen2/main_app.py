import click
import requests

url="http://127.0.0.1:8000/"

@click.command()
def get_pcap_list():
    result = requests.get(url+"getPcapList")
    print(result.json())


