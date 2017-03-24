import re


class AI:

    dust = None
    ass = None
    fint = None
    has_data = False
    has_unsent_data = False
    posts = []
    unsent_data = [] # stack-ish

    def __init__(self):
        s = open("stop_words.txt", "r")
        self.stop_words = s.read().split("\n")
        self.marks = [".", "?", "-", ",", "(", ")", "//", "///", "\\", ":", ";", "'", "=", "!", "#", "\xa0",
                      "%", "&", "$", "@", "ø", "æ", "å", "_", '"', "*"]
        self.html_words = ["<p>", "</p>", "\n", "<br />", "<em>", "</em>", "</strong>", "<strong>", "&nbsp;",
                           "<div>", "</div>", "<code>", "</code>", "<td>", "</td>", "</tr>", "<tr>", "<table>",
                           "</table>", "<t>"]
        # self.html_words = ["\n", "&nbsp;"]

    def set_fint(self, fint):
        self.fint = fint

    def set_dust(self, dust):
        self.dust = dust

    def set_ass(self, ass):
        self.ass = ass

    def run(self, fetch_new_data = False):
        print("AI STACK : " + str(len(self.unsent_data)))
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
                #print("ai sent data succ")
                if not self.unsent_data:
                    self.has_unsent_data = False
                    return
                return
        self.unsent_data.append(temp_data)

    def analyse(self):
        for posts in self.posts:
            y = posts[1]
            y = re.sub(r'<a.*?a>', '', y)
            y = re.sub(r'<.*?>', '', y)
            y = re.sub(r'<img.*?/>', '', y)
            y = re.sub(r'\&#.*?\;', '', y)
            for html in self.html_words:
                y = y.replace(html, "")
            for marks in self.marks:
                y = y.replace(marks, " ")
            piazza_post_arr = y.lower().split(" ")
            final_y = [x.strip() for x in piazza_post_arr if x not in self.stop_words
                       and not x.isdigit() and len(x) < 60]
            y_temp = set(final_y)
            '''delete_arr = []
            for norsk in y_temp:
                if "ø" in norsk or "æ" in norsk or "å" in norsk:
                    delete_arr.append(norsk)
            for norsk in delete_arr:
                y_temp.remove(norsk)'''
            percent = 0
            keyword_count = len(y_temp)
            if not keyword_count == 0:
                percent = 100/keyword_count
            key_prio = dict()
            for x in set(y_temp):
                key_prio.update({x: "%0.1f" % percent})
            self.unsent_data.append([posts[0], key_prio])
        self.has_unsent_data = True
        self.has_data = False

    def fetch_piazza(self, test = False):
        start_id = self.ass.get_highest_id()
        if not start_id:
            start_id = (("0", 0))
        if start_id:
            self.posts = []
            if test:
                self.posts = self.fint.update(cid = int(test))
            else:
                self.posts = self.fint.update(start_cid = start_id[0])
            if self.posts:
                self.has_data = True
                return True
        return False