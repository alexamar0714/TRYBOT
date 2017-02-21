import pymysql.cursors
import pymysql


class Mint:

    def connect(self, host='localhost', user='root', password='root', db='trybot'):
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

        :return: Connection

        '''

        try:
            # The connection
            connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
            return connection  # Returns the connection if successful
        except:
            return False  # Returns False if connection failed

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
            sql = "INSERT INTO keywords (word, priority, idinformation) VALUES (%s, %s, %s)"  # Query
            cursor.execute(sql, (word, priority, idinformation))  # Executes the query
            connection.commit()  # Commits the execution
            return True  # Returns True if adding successful
        except:
            return False  # Returns False if adding failed
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
            sql = "INSERT INTO information (idinformation, piazzaid) VALUES (%s, %s)"  # Query
            cursor.execute(sql, (idinformation, piazzaid))  # Executes the query
            connection.commit()  # Commits the execution
            return True  # Returns True if adding successful
        except:
            return False  # Returns False if adding failed
        finally:
            connection.close()  # Closes the connection to the database

    def get_all_keywords(self):
        '''

        Gets all rows of the keywords table

        :return: list of tuples

        '''

        connection = self.connect()  # Sets up a connection
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM keywords"  # Query
            cursor.execute(sql)  # Executes the query
            result = cursor.fetchall()
            return result  # Returns the result as a list of tuples if successful
        except:
            return False  # Returns False if getting failed
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
            return result  # Returns a list of tuples from the information table if successful
        except:
            return False  # Returns False if getting failed
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
            return result  # Returns a list of tuples with the wanted rows in the keyword table if successful
        except:
            return False  # Returns False if getting failed
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
            return result  # Returns the wanted row in the keyword table as a tuple if successful
        except:
            return False  # Returns False if getting failed
        finally:
            connection.close()  # Closes the connection to the database
            
    def get_highest_pri(self, soke_liste):
                '''

        Gets the piazzaIDs and sum of priority matching the words given in the array as input to the function 

        :type soke_liste: str array 
        :param soke_liste: eks ["sokeord1","sokeord2","sokeord3"]

        :return: List of tuples matching the input with desc sumpri, ((sumpri1,piazzaid1),(sumpri2,piazzaid2)): ((7,5738),(5,3245),(3,6578))
        '''
        
        connection = self.connect()
        cursor = connection.cursor()
        try:
            soke_string = "" #Makes an empty string to put in the sql statement 
            for word in soke_liste: #Builds the string to filter out words in the sql statement based on the input array
                soke_string+="word = '"+word+"' OR "
            soke_string = soke_string[:-3] #Removes the last OR
            #Joins the two tables, sum the prioreties, groups by the informationid and filters out the words.
            sql = "SELECT information.piazzaid, CAST(SUM(priority) AS UNSIGNED) AS sumpri FROM keywords INNER JOIN information ON keywords.idinformation = information.idinformation WHERE "+soke_string+" GROUP BY information.idinformation ORDER BY sumpri DESC LIMIT 3"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
