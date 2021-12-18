import json
import logger as lg
import requests


def alert(name, content, remote, address='http://127.0.0.1:8000/alert'):
    lg.output(f'ALERT - {name}\n{content}')
    if remote:
        try:
            requests.put(address, json={'name': name, 'content': content})
        except Exception:
            pass


def block(list_of_ip, address='http://127.0.0.1:8000/firewall'):
    try:
        requests.put(address, json={'list_of_ip': json.dumps(list_of_ip)})
    except Exception:
        pass
