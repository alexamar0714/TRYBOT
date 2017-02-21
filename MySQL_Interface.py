import pymysql.cursors
import PyMySQL

class Mint():

    def connect(self, host=str, user=str, password=str, db=str):
        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        return connection

    def set_keyword(self, word=str, priority=str, idinformation=str):
        connection = self.connect()
        try:
            sql = "INSERT INTO 'keywords' ('word', 'priority', 'idinformation') VALUES (%s, %s, %s)"
            connection.cursor(sql, (word, priority, idinformation))
            connection.commit()
        finally:
            connection.close()

    def set_information(self, idinformation, piazzaid):
        connection = self.connect()
        try:
            sql = "INSERT INTO 'information' ('idinformation', 'piazzaid) VALUES (%s, %s)"
            connection.cursor(sql, (idinformation, piazzaid))
            connection.commit()
        finally:
            connection.close()

    def get_all_keywords(self):
        connection = self.connect()
        try:
            sql = "SELECT '*' FROM 'keywords'"
            connection.cursor().execute(sql)
            result = connection.cursor().fetchall()
            print(result)
            return result
        finally:
            connection.close()
