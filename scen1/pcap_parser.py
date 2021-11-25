import pyshark as ps

from database import Database
from logger import Logger

db = Database()
logger = Logger(db)


def extract_traffic(path, filter):
    logger.log_a_logxd('LOG', f'extract_trafic({path}, {filter})')
    try:
        traffic = ps.FileCapture(path, display_filter=filter)
        print_traffic(traffic)
    except Exception as e:
        print(e)
        logger.log_a_logxd('ERROR', f'extract_trafic({path}, {filter}) - invalid path')

def print_traffic(traffic):
    for pcap in traffic:
        print(pcap)
