import os
import base64
import pickle
import unittest

from ..libs.knock import read_chain, write_chain


class TestKnock(unittest.TestCase):
    def test_read_chain(self):
        chain = [1, 2, 3, 4]
        with open('test_chain', 'wb') as f:
            f.write(base64.b64encode(pickle.dumps(chain)))
        self.assertEqual(read_chain('test_chain'), chain)

    def test_write_chain(self):
        chain = [1, 2, 3, 4]
        write_chain(chain, 'test_chain2')
        with open('test_chain2', 'rb') as f:
            encoded_chain = f.read()
        decoded_chain = base64.b64decode(encoded_chain)
        self.assertEqual(pickle.loads(decoded_chain), chain)

    def tearDown(self):
        try:
            os.remove('test_chain')
            os.remove('test_chain2')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()