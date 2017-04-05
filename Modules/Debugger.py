# pragma: no cover
from Fint import Fint
from Ass2 import Ass
from Mint2 import Mint
from AI import AI
from Dust import Dust
from PMS import PMS
import time
import pymysql


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
    fint_update_val = 10000000

    def __init__(self):  # pragma: no cover
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
        self.mint.set_connection(host = "localhost", user = "root", pw = "Admin", db = "trybot")
        self.fint.setup_connection(self.user, self.password, self.class_code)

    def run(self):  # pragma: no cover
        t = time.time()
        while True:
            self.ai.run()
            self.ass.run()
            self.dust.run()
            self.pms.run()
            print("AI data " + str(self.ai.has_data))
            print("AI uData " + str(self.ai.has_unsent_data))
            print("Ass data " + str(self.ass.has_data))
            print("Ass udata " + str(self.ass.has_unsent_data))
            print("dust data " + str(self.dust.has_data))
            print("dust udata " + str(self.dust.has_unsent_data))
            print("pms data " + str(self.pms.has_data))
            print("pms udata " + str(self.pms.has_unsent_data))
            x = input("click enter\n")
            if x == "exit":
                break
            if x[0:5] == "fetch":
                self.fint.setup_connection(self.user, self.password, self.class_code)
                self.ai.fetch_piazza(x[5:])
            if x[0:5] == "allup":
                self.fint.setup_connection(self.user, self.password, self.class_code)
                self.ai.fetch_piazza()
                loop = True
                while loop:
                    self.ai.run()
                    self.ass.run()
                    self.dust.run()
                    self.pms.run()
                    print("AI data " + str(self.ai.has_data))
                    print("AI uData " + str(self.ai.has_unsent_data))
                    print("Ass data " + str(self.ass.has_data))
                    print("Ass udata " + str(self.ass.has_unsent_data))
                    print("dust data " + str(self.dust.has_data))
                    print("dust udata " + str(self.dust.has_unsent_data))
                    print("pms data " + str(self.pms.has_data))
                    print("pms udata " + str(self.pms.has_unsent_data))
                    #print("\n\nCONNECTION TEST ")
                    #print(self.mint.get_highest_id())
                    print("\n\n")
                    if self.ai.loop() == 0:
                        loop = False
        t2 = time.time() - t
        m, s = divmod(t2, 60)
        print("%d : %d" %(m, s))

if __name__ == "__main__":
    main = Main()
    main.run()