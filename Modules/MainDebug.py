from Fint import Fint
from Ass2 import Ass
from Mint2 import Mint
from AI import AI
from Dust import Dust
from PMS import PMS
import time

class Main:

    mint = None
    Fint = None
    ass = None
    ai = None
    dust = None
    pms = None
    user = "alexamar@stud.ntnu.no"
    password = "Duongshit"
    class_code = "iy9ue7czifo1kk"
    fint_update_val = 600

    def __init__(self):
        self.fint = Fint()
        self.mint = Mint()
        self.ass = Ass()
        self.ai = AI()
        self.dust = Dust()
        self.pms = PMS()
        self.ass.set_pms(self.pms)
        self.ass.set_mint(self.mint)
        self.ai.set_fint(self.fint)
        self.ai.set_dust(self.dust)
        self.ai.set_ass(self.ass)
        self.dust.set_mint(self.mint)
        self.pms.set_fint(self.fint)

        #add something to get these as input?
        self.mint.set_connection(host = "localhost", user = "root", pw = "Admin", db = "trybot")
        self.fint.setup_connection(self.user, self.password, self.class_code)

    def run(self):
        while True:
            time.sleep(self.fint_update_val)
            self.fint.setup_connection()
            self.ai.fetch_piazza()
            stuck_count = 0
            current_stack = 0
            while True:
                self.ai.run()
                self.ass.run()
                self.dust.run()
                self.pms.run()
                x = self.ai.loop()
                if x == current_stack:
                    stuck_count += 1
                else:
                    current_stack = x
                    stuck_count = 0
                if stuck_count >= 3:
                    print("AI data " + str(self.ai.has_data))
                    print("AI uData " + str(self.ai.has_unsent_data))
                    print("Ass data " + str(self.ass.has_data))
                    print("Ass udata " + str(self.ass.has_unsent_data))
                    print("dust data " + str(self.dust.has_data))
                    print("dust udata " + str(self.dust.has_unsent_data))
                    print("pms data " + str(self.pms.has_data))
                    print("pms udata " + str(self.pms.has_unsent_data))
                    time.sleep(1)
                if x == 0:
                    break

if __name__ == "__main__":
    main = Main()
    main.run()