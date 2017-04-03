"""
This is the MysqlINTerface for the TRYBOT
The purpose of this module is to serve as the piazza post analyzer i.e "interpret" the posts content
"""


import pymysql.cursors
import pymysql


class Mint:

    """
    :type treshold: int
        :param Int value determines the lower limit of the sum(priority) of the answers
    :type host: str
        :param  Host name/ IP
    :type user: str
        :param Username used to connect to the database
    :type pw: str
        :param Password used to connect to the database
    :type db: str
        :param name of the database
    """

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
        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        return connection

    def add_keyword(self, word=str, priority=str, piazzaid=str):

        """
        Adds a keyword to the keyword table in the database

        :type word: str
            :param word: The keyword to add
        :type priority: str
            :param priority: The keyword's priority
        :type piazzaid: str
            :param piazzaid: The keyword's piazza id
        """

        try:
            connection = self.connect(self.host, self.user, self.pw, self.db)  # Sets up a connection to the database
            cursor = connection.cursor()
            # Basic idea: Insert new keyword if it does not exit in the table
            sql = "INSERT INTO KEYWORDS(WORD, PRIORITY, PIAZZAID) " \
                  "SELECT %s, %s, %s " \
                  "where not exists(select * from keywords " \
                  "where word = %s and piazzaid = %s)"  # Query
            cursor.execute(sql, (word, priority, piazzaid, word, piazzaid))  # Executes the query
            connection.commit()  # Commits the execution
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()

    def get_highest_pri(self, search_list):

        """
        Fetches the answer with highest count of words + prioirty sum

        :type search_list: dict
            :param search_list: a dictionary containing keywords + priority, only keywords are needed here
        """

        try:
            connection = self.connect(self.host, self.user, self.pw, self.db)
            cursor = connection.cursor()
            search_string = ""  # Makes an empty string to put in the sql statement
            for word in search_list:  # appends word to the search_string
                search_string += "word = '" + word + "' OR "
            search_string = search_string[:-3]  # Removes the last OR and space
            if len(search_string) <= 10:  # this happens if search_list contained nothing
                search_string = "word = 'putain'"  # hardcoded auto-FAIL search
            # basic idea, fetch based on SUM(Priority) > self.treshold AND return the answer with highest count(words)
            sql = "SELECT PIAZZAID FROM (SELECT PIAZZAID, SUM(PRIORITY) AS SUMMER FROM KEYWORDS" \
                  " WHERE " + search_string + " GROUP BY PIAZZAID) AS TEMP" \
                                            " JOIN (SELECT PIAZZAID AS PIAZZAID2, COUNT(PIAZZAID) AS COUNTER" \
                                            " FROM KEYWORDS" \
                                            " GROUP BY PIAZZAID) AS TEMP2" \
                                            " ON PIAZZAID = PIAZZAID2" \
                                            " WHERE SUMMER > %s ORDER BY COUNTER DESC LIMIT 1"
            cursor.execute(sql, self.threshold)
            result = cursor.fetchall()
            if len(result) != 0:  # check if there is a result, if not continue
                return result[0]
            # none found, return predefined string
            return "empty"
        except:
            return False
        finally:
            connection.close()

    def get_highest_id(self):

        """
        Fetches the highest post number and returns this
        """

        connection = self.connect(self.host, self.user, self.pw, self.db)
        cursor = connection.cursor()
        try:
            # basic idea: fetch the highest post number i.e piazzaId
            sql = "SELECT MAX(piazzaid) FROM keywords"
            cursor.execute(sql)
            return cursor.fetchall()  # if output ((int,))  else nothing i.e. tuple inside tuple
        except:
            return False
        finally:
            connection.close()
