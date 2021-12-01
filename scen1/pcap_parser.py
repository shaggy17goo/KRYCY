import pyshark as ps
import logger as lg

from database import Database
from logger import Logger

db = Database()
logger = Logger(db)


def extract_traffic(path, filter):
    logger.log_a_logxd('LOG', f'extract_trafic({path}, {filter})')
    try:
        traffic = ps.FileCapture(path, display_filter=filter)
        lg.output(traffic)
    except Exception as e:
        lg.output(e)
        logger.log_a_logxd('ERROR', f'extract_trafic({path}, {filter}) - invalid path')

def print_traffic(traffic):
    for pcap in traffic:
        lg.output(pcap)
