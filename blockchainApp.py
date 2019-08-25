import blockchainMain as main
import blockchainErrors as errors
import blockchainVerify as verify
from flask import Flask, request
import requests
import json
import datetime as date
"""
Networking and interaction
"""

app =  Flask(__name__)

blockchain = main.BlockChain()

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
		block_data["previous_hash"] = blockchain.last_block].hash
	except(IndexError):
		return "Coding error", 500
	block_data["index"] = len(blockchain.blocks)
	try:
		new_block = main.Block(block_data,blockchain.last_block)
		blockchain.append(new_block)
	except(errors.InvalidBlock):
		return "Block Invalid", 404
	except():
		return "Unknown Error", 404
	return "Success", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.blocks:
        chain_data.append(block.json)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/last_block', methods=['GET'])
def last_block():
	return (blockchain.last_block.json).replace("'",'"')

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
	new_block = main.Block(blockD, current_block)
	blockchain.append(new_block)
	
	return "Success", 201

@app.route('/get_user', methods=['GET'])
def get_user():
	user = request.args.get('username')
	block = blockchain.lastblock.json
	return "Not yet implemented", 418
	

app.run(debug=True, port=8000)