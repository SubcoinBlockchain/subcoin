import json, requests

try:
	dataF = open('postBlock.json', 'rb')
except:
	print("File may not exist, rename your new block to \"postBlock.json\"")
Jdata = json.load(dataF)
print(Jdata)
headers = {"content-type":"application/json"}
blockPost = requests.post('http://localhost:8000/new_block', headers = headers, data = json.dumps(Jdata))
print(blockPost.text)