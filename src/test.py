import unittest
from block import Block
from blockchain import Blockchain
from transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_1(self):
        tx = Transaction('A', 'B', 100)
        self.assertEqual(tx.sender, 'A')
        self.assertEqual(tx.to, 'B')
        self.assertEqual(tx.amount, 100)


class TestBlock(unittest.TestCase):
    def test_1(self):
        pass


class TestBlockchain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_new_tx(self):
        txs = [
            Transaction('0', 'A', 1000),
            Transaction('0', 'B', 500),
            Transaction('0', 'C', 900),
            Transaction('0', 'D', 5)
        ]
        b = Blockchain('node', txs, 'localhost:5000')
        b.new_transaction("A", "D", 1000)
        b.new_transaction("B", "D", 100)
        b.new_transaction("C", "D", 500)
        self.assertEqual(b.get_balance('A'), 1000)
        self.assertEqual(b.get_balance('B'), 500)
        self.assertEqual(b.get_balance('C'), 900)
        self.assertEqual(b.get_balance('D'), 5)
        self.assertEqual(len(b.mempool), 3)
        self.assertEqual(len(b.blocks), 1)

        # mine the txs creating a new block and emptying the pool
        b.mine()
        self.assertEqual(b.get_balance('A'), 0)
        self.assertEqual(b.get_balance('B'), 400)
        self.assertEqual(b.get_balance('C'), 400)
        self.assertEqual(b.get_balance('D'), 1605)
        self.assertEqual(len(b.mempool), 0)
        self.assertEqual(len(b.blocks), 2)

    def test_enough_balance_1(self):
        b = Blockchain('node', [], 'localhost:5000')
        b.new_transaction("A", "B", 1000)
        b.mine()
        # TODO: This should fail on get_balance level
        # TODO: and not allow negative balances
        self.assertEqual(b.get_balance('A'), -1000)

    def test_enough_balance_1(self):
        txs = [
            Transaction('0', 'A', 1000),
        ]
        b = Blockchain('node', txs, 'localhost:5000')
        b.new_transaction("A", "D", 1000)
        b.new_transaction("B", "D", 1000)

        # TODO: This should fail when mining. each transaction is valid
        # TODO: since the balance is enough, but both can't be recorded


if __name__ == '__main__':
    unittest.main()