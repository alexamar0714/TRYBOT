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
    
    alleKeywords = ((hei,5,2),(melk,1,2),(ole,1,2),(melk,7,3),(ole,1,4),(petter,1,3),(kopmis,20,50),(melk,1,8))
    alleInformation = ((2,4923),(3,9704),(4,8923),(5,5003),(6,7483))

    def initValues():
        mint = Mint()
        mint.connect(host,user,password,db)
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

        mint.close()

    def connection_test(self):
        mint = Mint()
        self.assertFalse(mint.connect('a', self.user, self.password, self.db))
        self.assertFalse(mint.connect(self.host, 'a', self.password, self.db))
        self.assertFalse(mint.connect(self.host, self.user, 'a', self.db))
        self.assertFalse(mint.connect(self.host, self.user, self.password, 'a'))

if __name__ == "__main__":
    unittest.main()
