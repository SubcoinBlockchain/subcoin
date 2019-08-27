import blockchainMain as main
import blockchainErrors as errors
import blockchainVerify as verify
from flask import Flask, request, render_template
import requests
import json
import datetime as date
import traceback

"""
Global Variables
"""
globalDiff = 1
app =  Flask(__name__)
blockchain = main.BlockChain('blockchain.json')
#blockchain = main.BlockChain()
"""
Administrative interactions
"""
@app.route('/adminset_difficulty', methods=['GET'])
def adminset_difficulty():
	try:
		difficulty = int(request.args.get('diff'))
	except(TypeError):
		return "NaN", 400
	except():
		return "?", 401
	globalDiff = difficulty
	return "", 201

"""
Networking and interaction
"""

@app.route('/new_block', methods=['POST'])
def new_block():
	block_data = {}
	try:
		block_data = request.get_json()
	except():
		return "Error", 500
	if(block_data == None):
		return "JSON not recieved", 404
	required_fields = ["data"]
	
	for field in required_fields:
		if not block_data.get(field):
			return "Invalid block data", 404
	if(verify.validateChanges(block_data,blockchain.last_block) != True):
	   raise InvalidChange
	block_data["timestamp"] = str(date.datetime.now())
	block_data["nonce"] = 0
	try:
		block_data["previous_hash"] = blockchain.last_block.hash
	except(IndexError):
		return "Coding error", 500
	block_data["index"] = len(blockchain.blocks)
	try:
		new_block = main.Block(block_data,blockchain.last_block, globalDiff)
		blockchain.append(new_block)
	except(errors.InvalidBlock):
		return "Block Invalid", 404
	except():
		return "Unknown Error", 404
	return "Success", 201

@app.route('/new_user', methods=['POST'])
def new_user():
	block_data = {}
	try:
		block_data = request.get_json()
	except():
		return "Error", 500
	if(block_data == None):
		return "JSON not recieved", 404
	required_fields = ["name","owner","orientation", "identifies_as"]
	for field in required_fields:
		if not block_data["data"][0]["users"][0].get(field):
			return "Invalid block data", 404
	current_block = blockchain.last_block
	blockD = main.buildBlockJson(block_data, current_block)
	new_block = main.Block(blockD, current_block, globalDiff)
	blockchain.append(new_block)
	
	return "Success", 201

@app.route('/new_userHTML', methods=['POST'])
def new_userHTML():
	block_data = {}
	current_block = blockchain.last_block
	try:
		form_data = json.dumps(request.form)
		block_data = json.loads(form_data)
	except():
		return "Error", 500
	if(block_data == None):
		return render_template("userFail.html", Herror="JSON not recieved"), 404
	if(type(block_data) == str):
		return render_template("userFail.html", Herror="JSON not parsed"), 500
	if(verify.validateUser(block_data, current_block) == False):
		return render_template("userFail.html", Herror = 'UserExists', user_name=block_data.get("name")), 400
	required_fields = ["name","owner","orientation", "identifies_as"]
	for field in required_fields:
		if not block_data.get(field):
			print("Invalid block data" + '\n' + json.dumps(block_data), 404)
			return render_template("userFail.html", error='Invalid block data')
	blockD = main.buildBlockUser(block_data, current_block)
	new_block = main.Block(blockD, current_block, globalDiff)
	blockchain.append(new_block)
	return render_template("userSuccess.html", user_name=block_data.get("name")), 200

"""
HTML interaction
"""
@app.route('/index')
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html"), 200

@app.route('/registeruser', methods=['GET'])
def registerUser():
	return render_template("registerUser.html"), 200

"""
Data retrieval
"""
@app.route('/last_block', methods=['GET'])
def last_block():
	blockD = json.loads(blockchain.last_block.json)
	return render_template('chain-block.html', block=blockD)

@app.route('/chain', methods=['GET'])
def get_chain():
	hash_chain = []
	for block in blockchain.blocks:
		block = json.loads(block.json)
		hash_chain.append(block["hash"])
	return render_template('chain.html', chain=hash_chain)

@app.route('/chain/<BHash>', methods=['GET'])
def chainHash(BHash):
	for block in blockchain.blocks:
		blockD = json.loads(block.json)
		if(blockD["hash"] == BHash):
			return render_template('chain-block.html', block=blockD)
		
	return "Not found", 404

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
	if(len(username) > 100):
		return "", 444
	blockData = json.loads(blockchain.last_block.json)["data"]
	users = []
	for user in blockData["users"]:
		users.append(user)
		if(user.get("name").lower() == username.lower()):
			if(user["owner"] != "NA" and user["owner"] != "None" and user["owner"] != None ):
				OData = user["owner"]
			else:
				OData = "None"
			return render_template('users-user.html', username=user["name"], gender=user["identifies_as"], orientation=user["orientation"], owner=OData ), 200
	return "Not found", 404

@app.route('/users', methods=['GET'])
def users():
	blockData = json.loads(blockchain.last_block.json)["data"]["users"]
	userlist = []
	for user in blockData:
		userlist.append(str(user["name"]))
	return render_template('users.html', users=userlist), 200
	
try:
	app.run(debug=True, port=8000)
except(KeyboardInterrupt):
	exit()