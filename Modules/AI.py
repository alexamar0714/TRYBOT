"""
This is the AnalyseInformation for the TRYBOT
The purpose of this module is to serve as the piazza post analyzer i.e "interpret" the posts content
"""

import re


class AI:

    """
        :type dust: Dust()-object
            :param The module that this module sends data to
        :type ass: Ass()-object
            :param The module that this module send data to
        :type Fint: Fint()-object
            :param The module used for fetching content from Piazza
        :type has_data: Boolean
            :param Tells if there is any data to be processed
        :type has_unsent_data: Boolean
            :param Tells if there is any processed data that has not been sent yet
        :type posts: List
            :param Data to be processed
        :type unsent_data: String
            :param Holds unsent processed data
    """

    dust = None
    ass = None
    fint = None
    has_data = False
    has_unsent_data = False
    posts = []
    unsent_data = [] # stack-ish

    def __init__(self):

        """
        Init all stop_words ie words to be removed from the piazza post
        """

        s = open("stop_words.txt", "r")
        self.stop_words = s.read().split("\n")
        s.close()
        self.marks = [".", "?", "-", ",", "(", ")", "//", "///", "\\", ":", ";", "'", "=", "!", "#", "\xa0",
                      "%", "&", "$", "@", "ø", "æ", "å", "_", '"', "*"]
        self.html_words = ["<p>", "</p>", "\n", "<br />", "<em>", "</em>", "</strong>", "<strong>", "&nbsp;",
                           "<div>", "</div>", "<code>", "</code>", "<td>", "</td>", "</tr>", "<tr>", "<table>",
                           "</table>", "<t>"]

    def set_fint(self, fint):

        """
        :type fint: Fint()-object
            :param fint:  Uses this Interface to fetch content from Piazza
        """

        self.fint = fint

    def set_dust(self, dust):

        """
        :type dust: Dust()-object
            :param dust: Sends data to this module
        """

        self.dust = dust

    def set_ass(self, ass):

        """
        :type ass: Ass()-object
            :param ass:  Sends data to this module
        """

        self.ass = ass

    def run(self, fetch_new_data = False):

        """
        Predefined run function that all modules used in cross-communication has, main uses this

        :type fetch_new_data: Boolean
            :param fetch_new_data: Used to tell this module if it should fetch new posts from piazza
        """

        if self.has_unsent_data:
            self.send_data()
            return True
        if self.has_data:
            self.analyse()
            return True
        if fetch_new_data:
            if self.fetch_piazza():
                return True
        return False

    def send_data(self):

        """
        This methods is used to send data to the other modules
        """

        temp_data = self.unsent_data.pop()  # pop from unsent stack
        if self.ass.set_data(temp_data):  # attempt to set_data on ass module
            if self.dust.set_data(temp_data):  # attempt to set_data on dust module
                if not self.unsent_data:  # check stack, if empty set has_unsent_data = False
                    self.has_unsent_data = False
                    return
                return  # unsent_data is not empty, therefore do nothing with has_unsent_data
        self.unsent_data.append(temp_data) # failed to set either ass or dust, therefore restack

    def analyse(self):

        """
        Strips the content from all unnecessary things and derives keywords from the content
        """

        for posts in self.posts:
            y = posts[1] # this is the post content as long string
            # remove statements
            y = re.sub(r'<a.*?a>', '', y)
            y = re.sub(r'<.*?>', '', y)
            y = re.sub(r'<img.*?/>', '', y)
            y = re.sub(r'\&#.*?\;', '', y)
            for html in self.html_words:
                y = y.replace(html, "")  # replace all self.html words with "" ie nothing
            for marks in self.marks:
                y = y.replace(marks, " ")  # replace all self.marks with " " ie space
            piazza_post_arr = y.lower().split(" ")
            # removes all trailing spaces + stop_words + digit and len() above 60
            final_y = [x.strip() for x in piazza_post_arr if x not in self.stop_words
                       and not x.isdigit() and len(x) < 60]
            y_temp = set(final_y)  # remove all duplicates
            percent = 0
            keyword_count = len(y_temp)
            if not keyword_count == 0:
                # our choice to calculate the priority of the words
                percent = 100/keyword_count
            key_prio = dict()
            for x in set(y_temp):
                key_prio.update({x: "%0.1f" % percent})
            self.unsent_data.append([posts[0], key_prio])
        self.has_unsent_data = True
        self.has_data = False

    def fetch_piazza(self, test = False):

        """
        Fetches content from piazza
        :type test: Str/Int
            :param test: used for fetching a precise post, mostly used for testing
        """

        start_id = self.ass.get_highest_id() # if output ((51,))  else nothing i.e. tuple inside tuple, num = int
        if not start_id:
            start_id = ((0, "tudulu"),) # if none/null StartId set to 0
        self.posts = []
        # this part is for testing, fetches single posts
        if test:
            self.posts = self.fint.update(cid = int(test))
        else:
            self.posts = self.fint.update(start_cid = str(start_id[0][0])) # magic happens here
        if self.posts:
            self.has_data = True
            return True
        return False

    def loop(self):
        """
        This method is used by main to determine if main should stop the main loop
        checks if self.unsent_data is empty (stack) if yes, return True else None
        """
        print("AI Stack: ", len(self.unsent_data))
        if not self.unsent_data:
            return 0
        return len(self.unsent_data)