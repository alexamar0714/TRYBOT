'''
This is the testing module for the MySQL Interface
'''

from Modules.Mint2 import Mint
import unittest


class TestMint(unittest.TestCase):

    host = "localhost"
    user = "root"
    password = "Admin"
    db = "trybot"
    keywords = [("a", "10", "1"), ("b", "10", "1"), ("c", "10", "1"),
                ("a", "9", "2"), ("b", "9", "2"), ("c", "9", "2"), ("d", "9", "2")]

    def test_set_connection(self):
        mint = Mint()
        mint.set_connection(self.host, self.user, self.password, self.db)
        self.assertEqual(mint.pw, self.password)
        self.assertEqual(mint.user, self.user)
        self.assertEqual(mint.host, self.host)
        self.assertEqual(mint.db, self.db)

    def test_add_keyword(self):
        mint = Mint()
        mint.set_connection(self.host, self.user, self.password, self.db)
        self.assertTrue(mint.add_keyword(self.keywords[0][0], self.keywords[0][1], self.keywords[0][2]))
        mint.set_connection("wrong", self.user, self.password, self.db)
        with self.assertRaises(UnboundLocalError):
            self.assertFalse(mint.add_keyword(self.keywords[0][0], self.keywords[0][1], self.keywords[0][2]))

    def test_get_highest_pri(self):
        mint = Mint()
        mint.set_connection(self.host, self.user, self.password, self.db)
        mint.threshold = 29
        for x in self.keywords:
            mint.add_keyword(x[0], x[1], x[2])
        self.assertEqual((1,), mint.get_highest_pri(["a", "b", "c"]))
        self.assertEqual((2,), mint.get_highest_pri(["a", "b", "c", "d"]))
        self.assertEqual("empty", mint.get_highest_pri([]))


if __name__ == "__main__":
    unittest.main()
