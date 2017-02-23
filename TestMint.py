self.'''
This is the testing module for the MySQL Interface
'''

from Mint import Mint
import unittest


class TestMint(unittest.TestCase):

    host = 'localhost'
    user = 'root'
    password = 'root'
    db = 'trybot'
    
    alle_keywords = ((hei,5,2),(melk,1,2),(ole,1,2),(melk,7,3),(ole,1,4),(petter,1,3),(kopmis,20,50),(melk,1,8))
    alle_information = ((2,4923),(3,9704),(4,8923),(5,5003),(6,7483))

    def initValues(self):
        mint = Mint()
        mint.addKeyWord("hei","5","2")
        mint.addKeyWord("melk","1","2")
        mint.addKeyWord("ole","1","2")
        mint.addKeyWord("melk","7","3")
        mint.addKeyWord("ole","1","4")
        mint.addKeyWord("petter","1","3")
        mint.addKeyWord("kompis","20","5")
        mint.addKeyWord("melk","1","8")

        mint.addInformation("2","4923")
        mint.addInformation("3","9704")
        mint.addInformation("4","8923")
        mint.addInformation("5","5003")
        mint.addInformation("6","7483")

    def connection_test(self):
        mint = Mint()
        self.assertFalse(mint.connect('a', self.user, self.password, self.db))
        self.assertFalse(mint.connect(self.host, 'a', self.password, self.db))
        self.assertFalse(mint.connect(self.host, self.user, 'a', self.db))
        self.assertFalse(mint.connect(self.host, self.user, self.password, 'a'))

    def input_output_test(self):
        mint = Mint()
        self.assertFalse(self.alel_keywords[0], mint.get_keyword_with_id("1"))
        self.initValues()
        self.assertEqual(self.alle_keywords, mint.get_keyword_with_id("1"))
        self.assertEqual(self.alle_keywords, mint.get_all_keywords())

if __name__ == "__main__":
    unittest.main()
