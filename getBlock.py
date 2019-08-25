import json, requests

data = {}
response = requests.get('http://localhost:8000/last_block')
data = response.json()
open('current.json', 'w').write(str(data))
