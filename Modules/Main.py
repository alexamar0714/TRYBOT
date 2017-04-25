from Fint import Fint
from Ass2 import Ass
from Mint2 import Mint
from AI import AI
from Dust import Dust
from PMS import PMS
import time

class Main:

    # --- Modify below ---
    user = ""  # Piazza user. Ex: "eksempel@stud.ntnu.no" NB: has to be enrolled to the class_code
    password = ""  # Piazza password. Ex: "MyPassword"
    # class code, found at the end of its URL Ex: https://piazza.com/class/(HERE IS THE CLASS CODE)
    class_code = "iy9ue7czifo1kk"  # Ex: "iy9ue7czifo1kk"
    fint_update_val = 10  # seconds of delay before fetching new data
    sqlUser = "root"  # name of sql user
    sqlPass = "Password"  # password of sql user
    sqlHost = "localhost"  # change this one if you use a different host
    # -------------------

    mint = None
    Fint = None
    ass = None
    ai = None
    dust = None
    pms = None
    
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

        self.mint.set_connection(host = self.sqlHost, user = self.sqlUser, pw = self.sqlPass, db = "trybot")
        self.fint.setup_connection(self.user, self.password, self.class_code)

    def run(self):
        while True:
            print("checking for new posts")
            time.sleep(self.fint_update_val)
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
