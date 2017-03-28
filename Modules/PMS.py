"""
This is the PostMachineSolution for the TRYBOT
The purpose of this module is to post the answer received from Ass() to piazza
"""


class PMS:

    """
    :type current_post: int
        :param the that it is currently on, i.e the post to be answered also used to check for answering several times
    :type data: int
        :param the answer post, i.e the answer to the current post
    :type has_data: Boolean
        :param tells if PMS has data to be "processed"
    :type fint: Fint()-object
        :param Interface used to post on piazza
    :type has_unsent_data: Boolean
        :param this is set if the first attempt at answering fails
    """

    current_post = None
    data = None
    has_data = False
    fint = None
    has_unsent_data = False

    def set_fint(self, fint):

        """
        :type fint: Fint()-object
            :param fint:  Interface used to post on piazza
        """

        self.fint = fint

    def set_data(self, current_post, answer_post):

        """
        receive data from Ass module

        :type current_post: int
            :param current_post: post Id of the question i.e the post that the answer_post is for
        :type answer_post: int
            :param answer_post:  answer post, i.e answer to the current_post
        """

        if not self.has_unsent_data and not self.has_data:
            if self.current_post == current_post:  # check if new post is the same as last post i.e don't answer
                self.has_data = False
                self.has_unsent_data = False
            else:
                self.data = answer_post
                self.current_post = current_post
                self.has_data = True
            return True
        return False

    def run(self):

        """
        Predefined run function that all modules used in cross-communication has, main uses this
        """

        if self.has_unsent_data:
            if self.fint.answer(cid = self.current_post, content = self.data):
                self.has_unsent_data = False
                return
        if self.has_data:
            if self.fint.answer(cid=self.current_post, content=self.data):
                self.has_data = False
            else:
                self.has_unsent_data = True
                self.has_data = False


