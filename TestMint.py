'''
This is the testing module for the MySQL Interface
'''

from Mint import Mint
import unittest


class TestMint(unittest.TestCase):

    host = 'localhost'
    user = 'root'
    password = 'root'
    db = 'trybot'

    def connection_test(self):
        mint = Mint()
        self.assertFalse(mint.connect('a', self.user, self.password, self.db))
        self.assertFalse(mint.connect(self.host, 'a', self.password, self.db))
        self.assertFalse(mint.connect(self.host, self.user, 'a', self.db))
        self.assertFalse(mint.connect(self.host, self.user, self.password, 'a'))

if __name__ == "__main__":
    unittest.main()
