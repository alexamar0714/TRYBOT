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
    data = None
    send_data = None
    has_unsent_data = False
    unsent_data = None
    AI = None
    PMS = None
    Mint = None

    def set_ai(self, ai):
        '''
        :param ai: The AI()-object to be used
        '''
        self.AI = ai

    def set_pms(self, pms):
        '''
        :param pms: The PMS()-object to be used
        '''
        self.PMS = pms

    def set_mint(self, mint):
        '''
        :param mint: The Mint()-object to be used
        '''
        self.Mint = mint

    def find_link(self):
        '''
        Finds the best answer for the post on Piazza
        '''
        self.send_data = self.Mint.get_highest_pri(self.data)
        self.send_data = self.send_data[0][0]

    def run(self):
        '''
        The main method that finds the answer and sends it to the PMS module.
        If sending the data is unsuccessful, the data is stored in a storage variable until it is successfully sent
        '''
        if self.has_data:
            self.find_link()
            check = self.PMS.set_data(self.send_data)  # check-variable used to see if the data is successfully sent
            self.has_data = False
            if not check:
                self.unsent_data = self.send_data
                self.has_unsent_data = True
            self.data = None
        if self.has_unsent_data:
            check = self.PMS.set_data(self.unsent_data)  # Same as the check-variable above
            if check:
                self.has_unsent_data = False
                self.unsent_data = None

    def set_data(self, data):
        '''
        :type data: String
        :param data: The data received from the AI module
        :return: returns True if data is successfully received, and false if not
        '''
        if not self.has_data and not self.has_unsent_data:
            self.data = data
            self.has_data = True
            return True
        else:
            return False