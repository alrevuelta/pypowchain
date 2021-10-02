from argparse import ArgumentParser
from flask import Flask, request
from blockchain import Blockchain
from threading import Thread
from transaction import Transaction
import time
import jsonpickle
from uuid import uuid4

app = Flask(__name__)

parser = ArgumentParser()
parser.add_argument('-p', '--port', default=5000, type=int, help='', required=True)
parser.add_argument('-m', '--mine', action='store_true')
parser.add_argument('-b', '--boot-node', default=None, type=str, help='')
parser.add_argument('-i', '--node-id', default=str(uuid4()).split('-')[0], type=str, help='')
args = parser.parse_args()

# initial balances
txs = [
    Transaction('0', 'A', 1000),
    Transaction('0', 'B', 1000)
]
blockchain = Blockchain(args.node_id, txs, f"localhost:{args.port}", boot_node=args.boot_node)

def mine():
    while True:
        blockchain.mine()
        time.sleep(1)

def resolve_split():
    while True:
        blockchain.resolve_split()
        time.sleep(10)

def gossip_peerstore():
    while True:
        blockchain.gossip_peerstore()
        time.sleep(10)

if args.mine:
    Thread(target=mine).start()
    Thread(target=resolve_split).start()
    Thread(target=gossip_peerstore).start()

Thread(target=app.run, args=('0.0.0.0', args.port)).start()


@app.route('/', methods=['GET'])
def index():
    node_info = f"Node_Id: {blockchain.node_id}\n" \
                f"Mempool: {blockchain.mempool}\n" \
                f"Peerstore: {blockchain.peerstore}\n" \
                f"Block: {blockchain.blocks}"
    return node_info, 200

# localhost:5000/addtx?sender=a&to=b&amount=100
@app.route('/addtx', methods=['GET'])
def addtx():
    sender = request.args.get('sender')
    to = request.args.get('to')
    amount = int(request.args.get('amount'))

    if None in [sender, to, amount]:
        return "Fields can't be empty", 500
    try:
        tx = blockchain.new_transaction(sender, to, amount)
    except Exception as e:
        return f"Error adding new tx: {e}"
    return f"Added tx to the pool: {tx}", 200

# localhost:5000/addblock?block=xx
@app.route('/addblock', methods=['GET'])
def addblock():
    block_serialized = request.args.get('block')
    if not block_serialized:
        return "Block field can't be empty", 500

    block = jsonpickle.decode(block_serialized)
    blockchain.add_block(block)
    return f"Added block to the blockchain: {block}", 200

# localhost:5000/addpeer?peer=localhost:5001
@app.route('/addpeer', methods=['GET'])
def addpeer():
    peer = request.args.get('peer')
    if not peer:
        return "Peer field can't be empty", 500
    blockchain.add_peer(peer)
    return f"Added peer: {peer}", 200

# localhost:5000/getlastblock
@app.route('/getlastblock', methods=['GET'])
def lastblock():
    return str(blockchain.blocks[-1]), 200

# localhost:5000/getblockchain
@app.route('/getblockchain', methods=['GET'])
def getblockchain():
    return str(jsonpickle.encode(blockchain.blocks)), 200

# localhost:5000/getpeerstore
@app.route('/getpeerstore', methods=['GET'])
def getpeers():
    return str(blockchain.peerstore), 200

# localhost:5000/getbalance?account=a
@app.route('/getbalance', methods=['GET'])
def getbalance():
    account = request.args.get('account')
    if not account:
        return "Account field can't be empty", 500

    balance = blockchain.get_balance(account)
    return f"The balance of {account} is {balance}", 200

# localhost:5000/getmempool
@app.route('/getmempool', methods=['GET'])
def getmempool():
    return str(blockchain.mempool), 200

# localhost:5000/mine
@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine()
    return f"Done mining, the proof is {str(block)}", 200

@app.route('/resolvesplit', methods=['GET'])
def resolvesplit():
    blockchain.resolve_split()
    return "Done", 200