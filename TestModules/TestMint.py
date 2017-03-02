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
    alle_keywords = (
    ("hei", 5, 2), ("melk", 1, 2), ("ole", 1, 2), ("melk", 7, 3), ("ole", 1, 4), ("petter", 1, 3), ("kompis", 20, 5),
    ("melk", 1, 8))

    alle_information = ((2, 4923), (3, 9704), (4, 8923), (5, 5003), (6, 7483))

    def initValues(self):
        mint = Mint()
        mint.add_keyword("hei", "5", "2")
        mint.add_keyword("melk", "1", "2")
        mint.add_keyword("ole", "1", "2")
        mint.add_keyword("melk", "7", "3")
        mint.add_keyword("ole", "1", "4")
        mint.add_keyword("petter", "1", "3")
        mint.add_keyword("kompis", "20", "5")
        mint.add_keyword("melk", "1", "8")

        mint.add_information("2", "4923")
        mint.add_information("3", "9704")
        mint.add_information("4", "8923")
        mint.add_information("5", "5003")
        mint.add_information("6", "7483")

    def test_connection(self):
        mint = Mint()
        self.assertFalse(mint.connect('a', self.user, self.password, self.db))
        self.assertFalse(mint.connect(self.host, 'a', self.password, self.db))
        self.assertFalse(mint.connect(self.host, self.user, 'a', self.db))
        self.assertFalse(mint.connect(self.host, self.user, self.password, 'a'))

    def test_input_output(self):
        mint = Mint()
        self.assertFalse(mint.get_keywords_with_information("2"))
        self.initValues()
   #    self.assertEqual(self.alle_keywords[0], mint.get_keywords_with_id("1"))
        self.assertEqual(self.alle_keywords, mint.get_all_keywords())
        self.assertEqual(self.alle_information, mint.get_all_information())
        self.assertEqual((('melk', 7, 3), ('petter', 1, 3)), mint.get_keywords_with_information("9704"))
        self.assertEqual(((5003,20), (9704, 7), (4923, 2)), mint.get_highest_pri(["melk", "ole", "kompis"]))


if __name__ == "__main__":
    unittest.main()
