import hashlib, json
import datetime as date
from flask import Flask, request
import requests
import blockchainErrors as errors

"""
Defining basic blockchain
"""

class BlockChain:
	blocks = []
	def __init__(self):
		with open('genesis.json','r') as json_file:
			block_genesis = json.load(json_file)
		genBlock = Block(block_genesis, '0')
		self.blocks.append(genBlock)
	def append(self, block):
		assert isinstance(block, Block), "Must pass a Block instance"
		self.blocks.append(block)
	
	@property
	def last_block(self):
		return self.blocks[len(self.blocks)-1]

class Block:
	difficulty = 1
	nonce = 0
	def __init__(self, json, last_block):
		self.nonce = json["nonce"]
		self.index = str(json["index"]).encode()
		self.timestamp = str(json["timestamp"]).encode()
		self.data = str(json["data"]).encode()
		self.previous_hash = str(json["previous_hash"]).encode()
		self.hash = self.hash_block()
		if(int(self.index) != 0):
			try:
				if(last_block.hash != self.previous_hash.decode()):
					print(str(self.previous_hash) + " : " + str(last_block.hash))
					raise errors.InvalidBlock
			except(IndexError):
				raise errors.CodeError

	def hash_block(self):
		sha = hashlib.sha256()
		sha.update( (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("utf-8") + str(self.nonce).encode() )
		
		while not sha.hexdigest().startswith('0'):
			self.nonce += 1
			sha.update( (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("utf-8") + str(self.nonce).encode() )
		return sha.hexdigest()
	
	@property
	def json(self):
		jsonD = {}
		jsonD["previous_hash"] = str(self.previous_hash.decode())
		jsonD["index"] = str(self.index.decode())
		jsonD["nonce"] = str(self.nonce)
		jsonD["timestamp"] = str(self.timestamp.decode())
		jsonD["data"] = str(self.data.decode())
		return (json.dumps(jsonD))

def next_block(last_block):
	jsonData = {}
	jsonData["index"] = int(last_block.index)+1
	jsonData["timestamp"] = date.datetime.now()
	jsonData["data"] = last_block.data.decode()
	jsonData["previous_hash"] = last_block.hash
	jsonData["nonce"] = 0
	return Block(jsonData)

def buildBlockJson(data, last_block):
	jsonD = {}
	#tmp = json.loads(data)
	#data = tmp
	oldJsonD = json.loads(last_block.json)
	jsonD["index"] = int(last_block.index)+1
	jsonD["timestamp"] = date.datetime.now()
	OJD = oldJsonD["data"].replace("'",'"')
	jsonD["data"] = json.loads(OJD)
	JData = jsonD["data"]
	Jusers = JData["users"]
	Jusers.append(data["data"][0]["users"][0])
	jsonD["previous_hash"] = last_block.hash
	jsonD["nonce"] = 0
	return jsonD
	
	