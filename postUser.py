import json, requests

try:
	dataF = open('postUser.json', 'rb')
except:
	print("File may not exist, rename your new block to \"postUser.json\"")
Jdata = json.load(dataF)
print(Jdata)
headers = {"content-type":"application/json"}
blockPost = requests.post('http://localhost:8000/new_user', headers = headers, data = json.dumps(Jdata))
print(blockPost.text)