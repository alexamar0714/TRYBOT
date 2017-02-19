"""
This is the ForumINTerface for the TRYBOT
The purpose of this module is to serve as an interface between the Bot and the Forum Piazza.
"""

import piazza_api


class Fint():

    def __init__(self):

        self._piazza = piazza_api.Piazza()

    def setup_connection(self, email, password, class_code):

        """
        Sets up a connection to piazza and the desired course

        :type  email: str
        :param email: The email used for connection

        :type  password: str
        :param password: The password used for connection

        :type  class_code: str
        :param class_code: The class' code, found at the end of its URL
        Ex: https://piazza.com/class/(HERE IS THE CLASS CODE)
        """

        try:
            self._piazza.user_login(email, password) #logs into piazza
            self._network = self._piazza.network(class_code) #establishes a connection to the specified class
            return True #returns true if successful

        except:
            return False #returns false if unsuccessful


    def update(self, start_cid=0, cid=None):

        """
        Goes through the Piazza posts, and if cid is declared, goes through only the specified post

        :type: cid: int
        :param: cid: Post ID

        :type: start_cid: int
        :param: start_cid: Update all posts with ID higher than start_cid
        """

        try:
            if cid: #if only one post is to be returned
                post = self._network.get_post(cid) #gets specified post from Piazza
                return [(post["nr"], post["history"][0]["content"])] #returns post number and content

            else:
                temp_arr = [] #temporary array that holds all the posts
                for x in self._network.iter_all_posts(): #loops through all posts

                    if x["nr"] > start_cid:
                        temp_arr.append((x["nr"], x["history"][0]["content"]))

                return temp_arr
        except:
            return False



    def answer(self, cid, content):

        """
        Posts a followup on Piazza

        :type: cid: int
        :param: cid: post ID

        :type: content: string
        :param: content: content of the followup
        """

        if content == None or isinstance(content, bool):
            return False

        elif isinstance(content, int): #if cid is an int, then produce a link to another post
            content = "@"+str(content)



        try:
            self._network.create_followup(self._network.get_post(cid), content, False)
            return True
        except:
            return False


