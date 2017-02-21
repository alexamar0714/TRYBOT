import pymysql.cursors
import pymysql


class Mint:

    def connect(self, host=str, user=str, password=str, db=str):
        '''

        Connects to the desired database

        :type host: str
        :param host: Host name/IP-address

        :type user: str
        :param user: User used to connect to the database

        :type password: str
        :param password: Users password

        :type db: str
        :param db: The database to connect to

        :return: Returns the connection
        '''

        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        return connection

    def add_keyword(self, word=str, priority=str, idinformation=str):
        '''

        Adds a keyword to the keyword table in the database

        :type word: str
        :param word: The keyword to add

        :type priority: str
        :param priority: The keyword's priority

        :type idinformation: str
        :param idinformation: The keyword's foreign key to the information table

        '''
        connection = self.connect()  # Sets up a connection to the database
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO keywords (word, priority, idinformation) VALUES (%s, %s, %s)"  # Query to be performed
            cursor.execute(sql, (word, priority, idinformation))  # Executes the query
            connection.commit()  # Commits the execution
        finally:
            connection.close()  # Closes the connection to the database

    def add_information(self, idinformation=str, piazzaid=str):
        '''

        Adds information to the information table in the database

        :type idinformation: str
        :param idinformation: The information id number

        :type piazzaid: str
        :param piazzaid: The id of the post on Piazza

        '''
        connection = self.connect()  # Sets up a connection to the database
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO information (idinformation, piazzaid) VALUES (%s, %s)"  # The query to be executed
            cursor.execute(sql, (idinformation, piazzaid))  # Executes the query
            connection.commit()  # Commits the execution
        finally:
            connection.close()  # Closes the connection to the database

    def get_all_keywords(self):
        '''

        Gets all the keywords with all their data

        :return: Returns a list of tuples with all keywords and their data

        '''

        connection = self.connect()  # Sets up a connection
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM keywords"  # The query to be executed
            cursor.execute(sql)  # Executes the query
            result = cursor.fetchall()
            return result  # Returns the result as a list of tuples
        finally:
            connection.close()  # Closes the connection to the database

    def get_all_information(self):
        '''

        Gets all the rows of the information table

        :return: List of tuples

        '''

        connection = self.connect()  # Sets up a connection to the database
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM information"  # Query
            cursor.execute(sql)  # Executes the quesry
            result = cursor.fetchall()
            return result  # Returns a list of tuples from the information table
        finally:
            connection.close()  # Close the connection

    def get_keywords_with_information(self, information_id=str):
        '''

        Gets all the rows in the keywords table with a specific information id

        :type information_id: str
        :param information_id: The information id of the wanted keywords

        :return: List of tuples
        '''
        connection = self.connect()  # Sets up a connection to the database
        cursor = connection.cursor()
        try:
            sql = "SELECT keywords.* FROM keywords,information WHERE keywords.idinformation =" + information_id  # Query
            cursor.execute(sql)  # Executes the query
            result = cursor.fetchall()
            return result  # Returns a list of tuples with the wanted rows in the keyword table
        finally:
            connection.close()  # Closes the connection to the database

    def get_keyword_with_id(self, index_id=str):
        '''

        Gets the row in the keyword table with specific id

        :type index_id: str
        :param index_id: The id of the wanted keyword

        :return: Tuple
        '''
        connection = self.connect()    # Sets up a connection to the database
        cursor = connection.cursor()
        try:
            sql = "SELECT keywords.* FROM keywords WHERE keywords.idkeywords =" + index_id  # Query
            cursor.execute(sql)  # Executes the query
            result = cursor.fetchall()
            return result  # Returns the wanted row in the keyword table as a tuple
        finally:
            connection.close()  # Closes the connection to the database
