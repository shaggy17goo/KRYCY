import requests

def alert(name, content, address='http://127.0.0.1:8000/alert'):
    print(f'ALERT - {name} - {content}')
    try: requests.put(address, json={'name': name, 'content': content})
    except Exception: pass