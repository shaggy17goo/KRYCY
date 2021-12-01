import os
import re
import logger as lg
from database import Database
from logger import Logger

extension = "\.(txt|py|xml|json)$"

db = Database()
logger = Logger(db)


def grep_via_x(file, pattern, re_or_grep):
    valid_path = re.search(extension, file)
    logger.log_a_logxd('LOG', f'grep_via_{re_or_grep}({file, pattern})')
    if not valid_path:
        lg.output("invalid file, only txt, py, xml, json extensions supported")
        logger.log_a_logxd('ERROR',
                           f'grep_via_{re_or_grep}({file, pattern}) - invalid file, only txt, py, xml, json extensions supported')
    elif not os.path.isfile(file):
        lg.output("file not found")
        logger.log_a_logxd('ERROR', f'grep_via_{re_or_grep}({file, pattern}) - file not found')
    else:
        if re_or_grep == 're':

            with open(file) as f:
                for line in f:
                    if re.search(pattern, line):
                        lg.output(line, end="")
        elif re_or_grep == 'grep':
            cmd = "cat " + file + " | grep -E \"" + pattern + "\""
            os.system(cmd)
