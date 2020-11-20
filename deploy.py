from web3 import HTTPProvider, Web3
import web3
import json

web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
if web3.isConnected():
	    print("Test net is connected")

web3.eth.defaultAccount = web3.eth.accounts[0]
trufflePath = 'contract'
truffleFile = json.load(open(trufflePath + '/build/contracts/Monopoly.json'))

abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

game = web3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = game.constructor().transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

if tx_receipt.status == 1:
	print("Contract deployed")
	print("Contract address:", tx_receipt.contractAddress)
