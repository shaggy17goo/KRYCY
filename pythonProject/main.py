import os
import re
import sqlite3



# DEBUGGING
from pythonProject.database import Database
from pythonProject.log import Log


def grep_via_re(path, regexp):
    filenamePattern = "^[^\0\/]{1,250}\.(txt|py|xml|json)$"
    validPath = re.match(filenamePattern, path)
    if not validPath:
        print("invalid filed, only txt, py, xml, json supported")
    elif not os.path.isfile(path):
        print("file not found")
    else:
        with open(path) as f:
            for line in f:
                if re.search(regexp, line):
                    print(line, end="")


def grep_via_grep(file, pattern):
    filenamePattern = "^[^\0\/]{1,250}\.(txt|py|xml|json)$"
    validPath = re.match(filenamePattern, file)
    if not validPath:
        print("invalid file, only txt, py, xml, json extensions supported")
    elif not os.path.isfile(file):
        print("file not found")
    else:
        cmd = "cat " + file + " | grep -E \"" + pattern + "\""
        os.system(cmd)


if __name__ == '__main__':
    database = Database()
    log = Log('ALERT', 'Wow wow, much alert, so secure')
    # database.add_data(log)
    print(database.get_data_by_id(10))
