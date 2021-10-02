# pypowchain

Simple Proof Of Work blockchain written in Python, to be used as a tool to explain how the core concepts of the technology work. Download and install depencies as follows. Python >3.6 must be used.

```console
git clone https://github.com/alrevuelta/pypowchain.git
cd pypowchain
pip3 install -r requirements.txt
cd src
python3 main.py -p 5000
```

## Run in debug mode

Runs a node on port `5000`. Note that the mining process has to be manually triggered.
```console
python3 main.py -p 5000
```

It exposes the following endpoints

```console
localhost:5000
localhost:5000/addtx?sender=A&to=B&amount=100
localhost:5000/addpeer?peer=localhost:5000
localhost:5000/getlastblock
localhost:5000/getblockchain
localhost:5000/getbalance?account=a
localhost:5000/getmempool
localhost:5000/getpeerstore
localhost:5000/mine
```

Other nodes can run in a different machine, where `boot-node` defines the entry point to the network, a node which is known.
```console
python3 main.py -p 5001 --boot-node=localhost:5000
```

It can be used as follows. After running a node with the command above, one can add a new transaction by a simple http get. It can be run in the browser or with `curl`. Note that accounts `A` and `B` contain some funds added in the genesis block.

```console
localhost:5000/addtx?sender=A&to=B&amount=100
```

After that, the transaction won't be recorded in the blockchain, but will be pending to be mined in the mempool. The mempool can be seen with, where we will see the pending transactions.

```console
localhost:5000/getmempool
```

With a non empty mempool, we are ready to mine the transactions. The consensus algorithim is Proof of Work. This command will find a number that meets a given criteria, and when its found, the mempool is flushed and all transactions are recorded in the blockchain.

```console
localhost:5000/mine
```

We can now see the new block with either:

```console
localhost:5000/getlastblock
localhost:5000/getblockchain
```

## Run in real time mode

By adding the flag `--mine` the node will continuously mine one block after another.
```console
python3 main.py -p 5000 --mine
```

It will also keep a mesh network with the rest of the peers, broadcasting the blocks that are mined and updating its blockchain if a longer one was detected in the network. Everything explained above applies, with the exception that there is no need to call mine.


# Test

```console
cd src
python3 -m unittest test
```
