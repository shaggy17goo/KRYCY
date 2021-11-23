import sqlite3

from scen1.database import Database
from scen1.log import Log

import searchUtilities

if __name__ == '__main__':
    searchUtilities.grep_via_grep('main.py', 'main')
