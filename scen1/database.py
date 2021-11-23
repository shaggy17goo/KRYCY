# sudo apt install sqlite3
# sudo apt install sqlitebrowser
import sqlite3


class Database:
    def __init__(self, database_file=None):
        if database_file is None:
            self.database_file = '../data/logsDatabase.sqbpro'
        self.con = None
        self.cur = None

    def connect_to_database(self):
        self.con = sqlite3.connect(self.database_file)
        self.cur = self.con.cursor()

    def disconnect_from_database(self):
        self.con.close()
        self.con = None
        self.cur = None

    def get_max_id(self):
        self.connect_to_database()
        sql_query = 'SELECT MAX(log_id) FROM logs'
        sql_query_result = self.cur.execute(sql_query)
        result = None
        for res in sql_query_result:
            result = res
        self.disconnect_from_database()
        if result is None:
            return -1
        return result[0]

    def add_data(self, log):
        max_log_id = self.get_max_id()
        self.connect_to_database()
        log.description = log.description.replace('\'', '')
        sql_query = f"INSERT INTO logs VALUES ({max_log_id+ 1},'{log.log_type}','{log.description}','{log.date}')"
        self.cur.execute(sql_query)
        self.con.commit()
        self.disconnect_from_database()

    def get_data_by_id(self, log_id):
        self.connect_to_database()
        sql_query = f"SELECT * FROM logs WHERE log_id == {log_id}"
        sql_query_result = self.cur.execute(sql_query)
        result = None
        for res in sql_query_result:
            result = res
            break
        self.disconnect_from_database()
        return result
