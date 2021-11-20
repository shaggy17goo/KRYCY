import requests

def alert(name, content, remote, address='http://127.0.0.1:8000/alert'):
    count = content.count('\n')
    print(f'ALERT ({count}) - {name}\n{content}')
    if remote:
        try: 
            requests.put(address, json={'name': name, 'content': content})
        except Exception: 
            pass