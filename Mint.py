import pymysql.cursors
import pymysql


class Mint():

    def connect(self, host="localhost", user="root", password="root", db="trybot"):
        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        return connection

    def add_keyword(self, word=str, priority=str, idinformation=str):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO 'keywords' ('word', 'priority', 'idinformation') VALUES (%s, %s, %s)"
            cursor.execute(sql, (word, priority, idinformation))
            connection.commit()
        finally:
            connection.close()

    def add_information(self, idinformation, piazzaid):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO 'information' ('idinformation', 'piazzaid) VALUES (%s, %s)"
            cursor.execute(sql, (idinformation, piazzaid))
            connection.commit()
        finally:
            connection.close()

    def get_all_keywords(self):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM keywords"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
     
    def get_all_information(self):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM information"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
