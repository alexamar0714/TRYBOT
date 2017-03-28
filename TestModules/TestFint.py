"""
This is the testing module for the ForumINTerface
"""


from Modules.Fint import Fint
import unittest


class TestFint(unittest.TestCase):

    email= "alexamar@stud.ntnu.no"
    password = "Duongshit"
    class_code = "iy9ue7czifo1kk"
    cid = 47

    def test_setup(self):
        fint = Fint()
        self.assertFalse(fint.setup_connection("", self.password, self.class_code))
        self.assertFalse(fint.setup_connection(12, self.password, self.class_code))
        self.assertFalse(fint.setup_connection(True, "1111", self.class_code))
        self.assertTrue(fint.setup_connection(self.email, self.password, self.class_code))

    def test_update(self):
        fint = Fint()
        self.assertFalse(fint.update())
        fint.setup_connection(self.email, self.password, self.class_code)
        self.assertFalse(fint.update(cid=1000))
        self.assertTrue(fint.update(cid=1))
        self.assertFalse(fint.update(cid="lol"))
        self.assertFalse(fint.update(start_cid="lol"))
        self.assertFalse(fint.update(start_cid=1000))
        self.assertTrue(fint.update(10))

    def test_answer(self):
        fint = Fint()
        self.assertFalse(fint.answer(self.cid, "blublub"))
        fint.setup_connection(self.email, self.password, self.class_code)
        self.assertFalse(fint.answer(True, "looool"))
        self.assertFalse(fint.answer("ddd", "fdf"))
        self.assertFalse(fint.answer(self.cid, True))
        self.assertFalse(fint.answer(self.cid, None))
        self.assertTrue(fint.answer(self.cid, "Unit test"))




if __name__ == "__main__":
    unittest.main()

