import sqlite3

from scen1.database import Database
from scen1.log import Log

if __name__ == '__main__':
    database = Database()
    log = Log('ALERT', 'Wow wow, much alert, so secure')
    # database.add_data(log)
    print(database.get_data_by_id(10))