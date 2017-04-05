from Modules.Fint import Fint
from Modules.PMS import PMS
import unittest


class TestPMS(unittest.TestCase):

    def test_set_fint(self):
        pms = PMS()
        fint = Fint()
        pms.set_fint(fint)
        self.assertEqual(fint, pms.fint)

    def test_set_data(self):
        pms = PMS()
        fint = Fint()
        pms.set_fint(fint)
        self.assertTrue(pms.set_data(current_post="1", answer_post="2"))
        self.assertFalse(pms.set_data(current_post="1", answer_post="2"))
        pms.has_data = False
        self.assertTrue(pms.set_data(current_post="1", answer_post="2"))
        self.assertFalse(pms.has_data)
        self.assertTrue(pms.set_data(current_post="3", answer_post="4"))

    def test_run(self):
        pms = PMS()
        fint = Fint()
        pms.set_fint(fint)
        pms.set_data("1", "2")
        pms.run()
        self.assertFalse(pms.has_data)
        pms.has_unsent_data = True
        pms.run()
        self.assertFalse(pms.has_unsent_data)
        self.assertFalse(pms.has_data)


if __name__ == "__main__":
    unittest.main()