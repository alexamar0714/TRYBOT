class Ass:

    '''
    Module for fetching/retrieving an appropriate solution to a question posted on Piazza.

    :type has_data: Boolean
    Tells if there is any data to be processed
    :type data: String
    Data to be processed
    :type send_data: String
    Processed data to be sent to next module
    :type has_unsent_data: Boolean
    Tells if there is any processed data that has not been sent yet
    :type unsent_data: String
    Holds unsent processed data
    :type AI: AI()-object
    The module that this module gets data from
    :type PMS: PMS()-object
    The module that this module send its data to
    :type Mint: Mint()-object
    The module used for performing queries to the database and getting the best result
    '''

    has_data = False
    data = None  # index 0 = ID, index 1 = keys
    has_unsent_data = False
    unsent_data = None
    PMS = None
    Mint = None

    def set_pms(self, pms):
        self.PMS = pms

    def set_mint(self, mint):
        self.Mint = mint

    def run(self):
        if self.has_unsent_data:
            if self.PMS.set_data(self.unsent_data[0], self.unsent_data[1]):
                self.has_unsent_data = False
            return
        if self.has_data:
            temp = self.Mint.get_highest_pri(self.data[1])
            if temp:
                if not self.PMS.set_data(self.data[0], temp):
                    self.has_unsent_data = True
                    self.unsent_data = [self.data[0], temp]
                self.has_data = False

    def set_data(self, data):
        if not self.has_data and not self.has_unsent_data:
            self.data = data
            self.has_data = True
            return True
        else:
            return False

    def get_highest_id(self):
        return self.Mint.get_highest_id()
