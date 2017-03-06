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
    data1 = None
    data2 = None
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
        if self.has_data:
            self.Mint.add_information(str(self.data1), str(self.data1))
            for word, priority in self.data2.items:
                self.Mint.add_keyword(word, priority, str(self.data1))

    def set_data(self, data):
        '''
        :param data: The data to be put into the database. Comes from the AI-module.
        Sets the parameter data if the module holds no data
        '''
        if not self.has_data:
            self.data1 = data[0]
            self.data2 = data[1]
            return True
        else:
            return False
