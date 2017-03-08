
from Fint import Fint
import re

class AI():

    has_data = False
    has_unsent_data = False
    posts = []
    unsent_data = [] # stack-ish

    def __init__(self):
        s = open("stop_words.txt", "r")
        self.stopp_words = s.read().split("\n")
        self.marks = [".", "?", "-", ",", "(", ")", "//", "///", "\\", ":", ";", "'", "=", "!", "#", "\xa0"]
        self.html_words = ["<p>", "</p>", "\n", "<br />", "<em>", "</em>", "</strong>", "<strong>", "&nbsp;"]
        self.fint = Fint()
        self.fint.setup_connection("", "", "iwvz8xg2t4o4c7")

    def run(self, fetch_new_data = False):
        if self.has_unsent_data:
            self.send_data()
            return True
        if self.has_data:
            self.analyse()
            return True
        if fetch_new_data:
            self.fetch_piazza()
            return True
        else: return False

    def send_data(self):
        if self.unsent_data:
            ###send to the fucker
            pass
        else:
            self.has_unsent_data = False

    def analyse(self):
        for posts in self.posts:
            y = posts[1]
            y = re.sub(r'<a.*?a>', '', y)
            y = re.sub(r'\&#.*?\;', '', y)
            for html in self.html_words:
                y = y.replace(html, "")
            for marks in self.marks:
                y = y.replace(marks, " ")
            piazza_post_arr = y.lower().split(" ")
            final_y = [x.strip() for x in piazza_post_arr if x not in self.stopp_words
                       and not x.isdigit()]
            y_temp = set(final_y)
            keyword_count = len(y_temp)
            precent = 100 / keyword_count
            key_prio = dict()
            for x in set(y_temp):
                key_prio.update({x: "%0.1f" % precent})
            self.unsent_data.append([posts[0], key_prio])
        self.has_unsent_data = True
        self.has_data = False
        for x in self.unsent_data:
            print(x)


    def fetch_piazza(self):
        #fetch highest ID from piazza
        pizza_id = 0
        self.posts = self.fint.update(start_cid = pizza_id)
        self.has_data = True




if __name__ == "__main__":
    ai = AI()
    ai.fetch_piazza()
    ai.analyse()