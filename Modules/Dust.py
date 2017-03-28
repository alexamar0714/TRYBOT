"""
This is the DatabaseUpdateSolutionTable for the TRYBOT
The purpose of this module is to update the database table
"""


class Dust:

    """
    :type has_data: Boolean
        :param has_data: Boolean to determine if it has data or not
    :type has_unsent_data: Boolean
        :param has_unsent_data: bool to determine if it has unsent processed data
    :type unsent_data: List
        :param unsent_data: [piazzaid, dict(keywords: priority)] this is set if first update fails
    :type data: List
        :param data: [piazzaid, dict(keywords: priority)]
    :type mint: Mint()-object
        :param mint: the interface used to update/append new keywords
    """

    has_data = False
    has_unsent_data = False
    unsent_data = None
    data = None  # index 0 = piazzaID, index 1 = Keywords
    Mint = None

    def set_mint(self, mint):

        '''
        :type mint: Mint()-object
            :param mint: used for communicating with the database
        '''

        self.Mint = mint

    def run(self):

        '''
        Predefined run function that all modules used in cross-communication has, main uses this
        '''

        if self.has_unsent_data:
            # failed first time, retries now
            val = self.process_data()
            if val == len(self.data[1]):  # check if ALL keywords have been inserted into the database
                self.has_unsent_data = False
                self.has_data = False
                return True
            return False

        if self.has_data:
            val = self.process_data()
            if val == len(self.data[1]): # check if ALL keywords have been inserted into the database
                self.has_data = False
                return True
            self.has_unsent_data = True
            self.unsent_data = self.data
            self.has_data = False
            return False

    def process_data(self):

        """
        Loops through the dictionary and attempts to update the database with the tulpes. For each successful update
         it adds +1 to the variable successful, this variable is used by run()
        """

        successful = 0
        for word, priority in self.data[1].items():
            if self.Mint.add_keyword(word, priority, str(self.data[0])):
                successful += 1
                continue
            break
        return successful

    def set_data(self, data):

        """
        :type data: List
        :param data: [piazzaid, dict(keywords: priority)]
        """

        if not self.has_data and not self.has_unsent_data:
            self.data = data
            self.has_data = True
            return True
        else:
            return False
