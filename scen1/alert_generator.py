import requests
import json

def alert(name, content, remote, address='http://127.0.0.1:8000/alert'):
    count = content.count('\n')
    print(f'ALERT ({count}) - {name}\n{content}')
    if remote:
        try:
            requests.put(address, json={'name': name, 'content': content})
        except Exception:
            pass


def block(list_of_ip, address='http://127.0.0.1:8000/firewall'):
    requests.put(address, json={'list_of_ip': json.dumps(list_of_ip)})


if __name__ == '__main__':
    block(['10.0.0.10', '10.0.0.16'])
