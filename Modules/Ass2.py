"""
This is the AccessStoredSolutions for the TRYBOT
The purpose of this module is to fetch stored data from the database
"""


class Ass:

    """
    :type has_data: Boolean
        :param Tells if there is any data to be processed
    :type data: List
        :param [piazzaid, dict(keywords: priority)] this is data to be processed
    :type has_unsent_data: Boolean
        :param Tells if there is any processed data that has not been sent yet
    :type unsent_data: String
        :param Holds unsent processed data
    :type pms: PMS()-object
        :param The module that this module send its data to
    :type mint: Mint()-object
        :param The module used for performing queries to the database and getting the highest match
    """

    has_data = False
    data = None  # index 0 = ID, index 1 = keys
    has_unsent_data = False
    unsent_data = None
    pms = None
    mint = None

    def set_pms(self, pms):

        """
        :type pms: PMS()-object
            :param pms: Sends data to this module
        """

        self.pms = pms

    def set_mint(self, mint):

        """
        :type mint: Mint()-object
            :param mint: Sends data to this module
        """

        self.mint = mint


    def run(self):

        """
        Predefined run function that all modules used in cross-communication has, main uses this
        """

        if self.has_unsent_data:
            if self.pms.set_data(self.unsent_data[0], self.unsent_data[1]):
                self.has_unsent_data = False
            return
        if self.has_data:
            temp = self.mint.get_highest_pri(self.data[1])
            if temp == "empty":  # hardcoded response
                temp = [self.data[0], "tudulu"]  # tudulu has no meaning, placeholder at most
            if temp[0] == int(self.data[0]):  # if answer piazzaid is equal to current piazzaid, then ignore
                self.has_data = False
                return
            if not self.pms.set_data(self.data[0], temp[0]):
                self.has_unsent_data = True
                self.unsent_data = [self.data[0], temp[0]]
            self.has_data = False

    def set_data(self, data):

        """
        Receives data from other modules

        :type data: List
            :param data: (piazzaId, dict(keywords : priority))
        """

        if not self.has_data and not self.has_unsent_data:
            self.data = data
            self.has_data = True
            return True
        else:
            return False

    def get_highest_id(self):

        """
        Uses Mint module to get the highest piazza post ID
        """

        return self.mint.get_highest_id()
