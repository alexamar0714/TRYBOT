
from Fint import Fint
import re


class AI:

    dust = None
    ass = None

    has_data = False
    has_unsent_data = False
    posts = []
    unsent_data = [] # stack-ish

    def __init__(self):
        s = open("stop_words.txt", "r")
        self.stop_words = s.read().split("\n")
        self.marks = [".", "?", "-", ",", "(", ")", "//", "///", "\\", ":", ";", "'", "=", "!", "#", "\xa0"]
        self.html_words = ["<p>", "</p>", "\n", "<br />", "<em>", "</em>", "</strong>", "<strong>", "&nbsp;"]
        self.fint = Fint()
        self.fint.setup_connection("", "", "iwvz8xg2t4o4c7")

    def set_dust(self, dust):
        self.dust = dust

    def set_ass(self, ass):
        self.ass = ass

    def run(self, fetch_new_data = False):
        if self.has_unsent_data:
            self.send_data()
            return True
        if self.has_data:
            self.analyse()
            return True
        if fetch_new_data:
            if self.fetch_piazza():
                return True # string? to know that main should keep asking?
        return False

    def send_data(self):
        temp_data = self.unsent_data.pop()
        if self.ass.set_data(temp_data):
            if self.dust.set_data(temp_data):
                if not self.unsent_data:
                    self.has_unsent_data = False
                    return
        self.unsent_data.append(temp_data)

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
            final_y = [x.strip() for x in piazza_post_arr if x not in self.stop_words
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
        start_id = self.ass.get_highest_id()
        if start_id:
            self.posts = []
            self.posts = self.fint.update(start_cid = start_id)
            if self.posts:
                self.has_data = True
                return True
        return False


if __name__ == "__main__":
    ai = AI()
    ai.fetch_piazza()
    ai.analyse()