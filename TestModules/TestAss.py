from Modules.Ass2 import Ass
from Modules.Mint2 import Mint
from Modules.PMS import PMS
import unittest


class TestAss(unittest.TestCase):

    def test_get_highest_id(self):
        mint = Mint()
        ass = Ass()
        ass.set_mint(mint)
        with self.assertRaises(Exception):
            ass.get_highest_id()
        mint.set_connection(host = "localhost", user = "root", pw = "Admin", db = "trybot")
        self.assertNotEqual(None, ass.get_highest_id())

    def test_set_pms(self):
        pms = PMS()
        ass = Ass()
        ass.set_pms(pms)
        self.assertEqual(pms, ass.pms)

    def test_set_mint(self):
        mint = Mint()
        ass = Ass()
        ass.set_mint(mint)
        self.assertEqual(mint, ass.mint)

    def test_set_data(self):
        ass = Ass()
        self.assertTrue(ass.set_data("1"))
        self.assertFalse(ass.set_data("2"))
        ass.has_data = False
        ass.has_unsent_data = True
        self.assertFalse(ass.set_data("3"))

    def test_run(self):
        ass = Ass()
        mint = Mint()
        mint.set_connection(host = "localhost", user = "root", pw = "Admin", db = "trybot")
        pms = PMS()
        ass.set_pms(pms)
        ass.set_mint(mint)
        mint.add_keyword(word="testcode", priority="100", piazzaid="235")
        self.assertTrue(ass.set_data(["230", {"testcode": 100}]))
        ass.run()
        self.assertFalse(pms.set_data("235", "235"))
        pms.has_data = False
        self.assertTrue(ass.set_data(["235", {"testcode": 100}]))
        ass.run()
        self.assertTrue(pms.set_data("235", "235"))
        self.assertTrue(ass.set_data(["230", {"testcode": 100}]))
        ass.run()
        self.assertFalse(ass.set_data(["230", {"testcode": 100}]))
        pms.has_data = False
        ass.run()
        self.assertTrue(ass.set_data([["230", {"testcode": 100}]]))

if __name__ == "__main__":
    unittest.main()