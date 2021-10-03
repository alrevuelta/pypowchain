from block import Block
from random import randint
from transaction import Transaction
import hashlib
import time
import requests
import jsonpickle


class Blockchain:
    def __init__(self, node_id, init_txs, host, boot_node=None):
        self.node_id = node_id
        self.mempool = []
        self.host = host
        self.blocks = [Block(0, "genesis_block", 0, "0", init_txs)]
        self.peerstore = set()
        self.peerstore.add(host)
        if boot_node:
            self.add_peer(boot_node)

    def new_transaction(self, sender, to, amount):
        balance = self.get_balance(sender)
        if amount > balance:
            raise Exception("not enough balance", amount, balance)
        tx = Transaction(sender, to, amount)
        self.mempool.append(tx)
        return tx

    def get_balance(self, account):
        balance = 0
        for block in self.blocks:
            for tx in block.txs:
                if tx.sender == account:
                    balance -= tx.amount
                elif tx.to == account:
                    balance += tx.amount
        return balance

    def gossip_peerstore(self):
        for peer in self.peerstore.copy():
            for peer_info in self.peerstore.copy():
                if peer != peer_info and peer != self.host:
                    url = f'http://{peer}/addpeer?peer={peer_info}'
                    try:
                        requests.get(url)
                    except Exception as e:
                        # TODO: Prune erroring peers
                        print("Error", e)

    def resolve_split(self):
        for peer in self.peerstore:
            if peer == self.host:
                continue
            url = f'http://{peer}/getblockchain'
            try:
                blockchain = requests.get(url)
                blocks = jsonpickle.decode(blockchain.text)

                # Use always the longest chain
                if len(blocks) > len(self.blocks):
                    # TODO: Check that the blocks are valid
                    self.blocks = blocks
            except Exception as e:
                print("Error", e)

    def add_peer(self, peer_host):
        self.peerstore.add(peer_host)

    def mine(self):
        proof = 0
        while not self.is_valid_proof(self.blocks[-1], proof):
            proof = randint(0, 100000)
            time.sleep(0.05)

        # once the proof is found, create new block with txs in the pool
        new_index = self.blocks[-1].index + 1
        block = Block(new_index, self.node_id, proof, self.blocks[-1].hash, self.mempool)

        # add a reward for the miner
        block.txs.append(Transaction('0', self.node_id, 50))

        self.add_block(block)
        self.mempool = []

        print("New block", block)

        # broadcast block
        self.broadcast_block(block)

        return block

    def add_block(self, block):
        # TODO run more checks
        # TODO handle blocks out of order
        if self.blocks[-1].hash == block.prev_hash:
            self.blocks.append(block)

    def broadcast_block(self, block):
        for peer in self.peerstore:
            if peer == self.host:
                continue
            url = f'http://{peer}/addblock?block={jsonpickle.encode(block)}'
            try:
                requests.get(url)
            except Exception as e:
                print("Error", e)

    def is_valid_proof(self, last_block, proof):
        guess = f'{last_block.proof}{proof}{last_block.hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # TODO: Set variable difficulty
        return guess_hash[:2] == "00"