import blockchainMain as main
import blockchainErrors as errors
import json

def validateChanges(new_block, current_block):
	if not new_block["data"].get("users"):
		return False
	
	return True