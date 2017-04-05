from Modules.Dust import Dust
from Modules.Mint2 import Mint
import unittest


class TestDust(unittest.TestCase):

    def test_set_mint(self):
        dust = Dust()
        mint = Mint()
        dust.set_mint(mint)
        self.assertEqual(mint, dust.mint)

    def test_set_data(self): # also tests method process_data()
        dust = Dust()
        mint = Mint()
        dust.set_mint(mint)
        mint.set_connection(host="wrooong", user="root", pw="Admin", db="trybot")
        self.assertTrue(dust.set_data(["1", {"test": 100}]))
        self.assertFalse(dust.set_data(["2", {"test": 100}]))
        with self.assertRaises(Exception):
            dust.run()
        self.assertFalse(dust.set_data(["3", {"test": 100}]))
        mint.set_connection(host="localhost", user="root", pw="Admin", db="trybot")
        dust.run()
        self.assertTrue(dust.set_data(["4", {"test": 100}]))

    def test_run(self):
        dust = Dust()
        mint = Mint()
        dust.set_mint(mint)
        mint.set_connection(host="wrooong", user="root", pw="Admin", db="trybot")
        self.assertTrue(dust.set_data(["1", {"test": 100}]))
        with self.assertRaises(Exception):
            self.assertFalse(dust.run())  # has_data = True
            self.assertFalse(dust.run())  # has_unsent_data = True
        mint.set_connection(host="localhost", user="root", pw="Admin", db="trybot")
        self.assertTrue(dust.run())
        self.assertTrue(dust.set_data(["3", {"test": 100}]))
        self.assertTrue(dust.run())


if __name__ == "__main__":
    unittest.main()