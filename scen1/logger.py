import database as db
import log as lg


class Logger:
    def __init__(self, database):
        self.database = database

    def log_a_logxd(self, log_type, description):
        log = lg.Log(log_type, description)
        self.database.add_data(log)
        print(log)