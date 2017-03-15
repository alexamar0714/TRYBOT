class Dust:

    '''
    :type has_data: Boolean
    Tells if the module has any data to be processed
    :type data1: int
    Holds the Piazza-link
    :type data2: Dictionary
    Holds the keywords corresponding the Piazza-link
    :type Mint: The Mint()-object used to insert/update the database
    '''

    has_data = False
    has_unsent_data = False
    unsent_data = None
    data = None  # index 0 = piazzaID, index 1 = Keywords
    Mint = None

    def set_mint(self, mint):
        '''
        :param mint: The Mint()-object used for communicating with the database
        '''
        self.Mint = mint

    def run(self):
        '''
        The main function of this module. If the module holds any data, it inserts it into the database.
        '''
        if self.has_unsent_data:
            val = self.process_data()
            if val == len(self.data[1]):
                self.has_unsent_data = False
                self.has_data = False
                return True
            return False

        if self.has_data:
            val = self.process_data()
            #print("this is values : " + str(val))
            #print("this is length : " + str(len(self.data[1])))
            if val == len(self.data[1]):
                self.has_data = False
                return True
            self.has_unsent_data = True
            self.unsent_data = self.data
            self.has_data = False
            return False

    def process_data(self):
        successful = 0
        for word, priority in self.data[1].items():
            if self.Mint.add_keyword(word, priority, str(self.data[0])):
                successful += 1
                continue
            break
        return successful

    def set_data(self, data):
        '''
        :param data: The data to be put into the database. Comes from the AI-module.
        Sets the parameter data if the module holds no data
        '''
        if not self.has_data and not self.has_unsent_data:
            self.data = data
            self.has_data = True
            return True
        else:
            return False
