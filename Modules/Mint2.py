import pymysql.cursors
import pymysql


class Mint:

    threshold = 80
    host = ""
    user = ""
    pw = ""
    db = ""

    def set_connection(self, host, user, pw, db):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db

    def connect(self, host, user, password, db):
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

            # The connection
        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        return connection  # Returns the connection if successful


    def add_keyword(self, word=str, priority=str, piazzaid=str):
        '''
        Adds a keyword to the keyword table in the database
        :type word: str
        :param word: The keyword to add
        :type priority: str
        :param priority: The keyword's priority
        :type piazzaid: str
        :param piazzaid: The keyword's foreign key to the information table
        '''
        try:
            connection = self.connect(self.host, self.user, self.pw, self.db)  # Sets up a connection to the database
            cursor = connection.cursor()
            sql = "INSERT INTO KEYWORDS(WORD, PRIORITY, PIAZZAID) " \
                  "SELECT %s, %s, %s " \
                  "where not exists(select * from keywords " \
                  "where word = %s and piazzaid = %s)"  # Query
            cursor.execute(sql, (word, priority, piazzaid, word, piazzaid))  # Executes the query
            connection.commit()  # Commits the execution
            return True
        except:
            return False
        finally:
            connection.close()

    def get_highest_pri(self, soke_liste):
        '''
        Gets the piazzaIDs and sum of priority matching the words given in the array as input to the function
        :type soke_liste: str array
        :param soke_liste: eks ["sokeord1","sokeord2","sokeord3"]
        :return: List of tuples matching the input with desc sumpri, ((sumpri1,piazzaid1),(sumpri2,piazzaid2)): ((7,5738),(5,3245),(3,6578))
        '''
        try:
            connection = self.connect(self.host, self.user, self.pw, self.db)
            cursor = connection.cursor()

            soke_string = ""  # Makes an empty string to put in the sql statement
            for word in soke_liste:  # Builds the string to filter out words in the sql statement based on the input array
                soke_string += "word = '" + word + "' OR "
            print("error 1")
            soke_string = soke_string[:-3]  # Removes the last OR
            if len(soke_string) <= 10:
                print("error 2")
                soke_string = "word = 'putain'"
            # Joins the two tables, sum the prioreties, groups by the informationid and filters out the words.
            sql = "SELECT PIAZZAID FROM (SELECT PIAZZAID, SUM(PRIORITY) AS SUMMER FROM KEYWORDS" \
                  " WHERE " + soke_string + " GROUP BY PIAZZAID) AS TEMP" \
                                            " JOIN (SELECT PIAZZAID AS PIAZZAID2, COUNT(PIAZZAID) AS COUNTER FROM KEYWORDS" \
                                            " GROUP BY PIAZZAID) AS TEMP2" \
                                            " ON PIAZZAID = PIAZZAID2" \
                                            " WHERE SUMMER > %s ORDER BY COUNTER DESC LIMIT 1"
            cursor.execute(sql, (self.threshold))
            result = cursor.fetchall()
            if len(result) != 0:
                return result[0]
            # none found
            return "empty"
        except:
            return False
        finally:
            connection.close()




    def get_highest_id(self):
        connection = self.connect(self.host, self.user, self.pw, self.db)
        cursor = connection.cursor()
        try:
            sql = "SELECT MAX(piazzaid) FROM keywords"
            cursor.execute(sql)
            return cursor.fetchall()
        except:
            return False
        finally:
            connection.close()
