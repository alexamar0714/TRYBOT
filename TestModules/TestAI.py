from Modules.AI import AI
from Modules.Ass2 import Ass
from Modules.Dust import Dust
from Modules.Fint import Fint
from Modules.Mint2 import Mint
import unittest


class TestAI(unittest.TestCase):

    user = "alexamar@stud.ntnu.no"
    password = "Duongshit"
    class_code = "iy9ue7czifo1kk"

    def test_set_fint(self):
        ai = AI()
        fint = Fint()
        ai.set_fint(fint)
        self.assertEqual(fint, ai.fint)

    def test_set_dust(self):
        ai = AI()
        dust = Dust()
        ai.set_dust(dust)
        self.assertEqual(dust, ai.dust)

    def test_set_ass(self):
        ai = AI()
        ass = Ass()
        ai.set_ass(ass)
        self.assertEqual(ass, ai.ass)

    def test_loop(self):
        self.tearDown()
        fint = Fint()
        fint.setup_connection(self.user, self.password, self.class_code)
        ai = AI()
        ai.set_fint(fint)
        ass = Ass()
        ass.set_mint(Mint())
        ai.set_ass(ass)
        ass.mint.set_connection(host = "localhost", user = "root", pw = "Admin", db = "trybot")
        ai.unsent_data = []
        self.assertEqual(0, ai.loop())
        ai.fetch_piazza(test = 1)
        ai.run()
        self.assertEqual(1, ai.loop())

    def test_fetch_piazza(self):
        fint = Fint()
        fint.setup_connection(self.user, self.password, self.class_code)
        ai = AI()
        ai.set_fint(fint)
        ass = Ass()
        ass.set_mint(Mint())
        ai.set_ass(ass)
        ass.mint.set_connection(host="localhost", user="root", pw="Admin", db="trybot")
        self.assertEqual(0, ai.loop())
        self.assertTrue(ai.fetch_piazza(test = 50))
        ai.run()
        self.assertNotEqual(0, ai.loop())
        ai.set_dust(Dust())
        ai.run()
        ai.fetch_piazza()
        ai.run()
        self.assertNotEqual(0, ai.loop())

    def test_send_data(self):
        ai = AI()
        dust = Dust()
        ass = Ass()
        ai.set_ass(ass)
        ai.set_dust(dust)
        ai.unsent_data = []
        ai.unsent_data.append(["1", {"test": 1}])
        self.assertTrue(ai.send_data())
        self.assertEqual(0, ai.loop())
        ai.unsent_data.append(["1", {"test": 1}])
        self.assertFalse(ai.send_data())
        self.assertEqual(1, ai.loop())



if __name__ == "__main__":
    unittest.main()