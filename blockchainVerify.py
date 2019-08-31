import blockchainMain as main
import blockchainErrors as errors
import json

def validateChanges(new_block, current_block):
	if not new_block["data"].get("users"):
		return False
	return True
	
def validateUser(username, current_block):
	data = json.loads(current_block.json)["data"]["users"]
	for user in data:
		name = user["name"]
		if(str(name).lower() == username["name"].lower()):
		   return False
	return True