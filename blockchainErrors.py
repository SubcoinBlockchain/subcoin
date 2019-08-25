"""
Custom errors
"""
class BlockchainError(Exception):
	pass
class InvalidBlock(BlockchainError):
	pass
class InvalidChange(BlockchainError):
	pass
class CodeError(BlockchainError):
	pass
