import json
import re
import xml.sax
import pyshark as ps
import Evtx.Evtx as evtx

from database import Database
from logger import Logger

db = Database()
logger = Logger(db)


def validate_text_encoding(**kwargs):
    if kwargs['files']['pcap'] or kwargs['files']['evtx'] or kwargs['files']['json'] or kwargs['files']['xml']:
        # print(f'Some unsupported files were provided! This rule works only for txt files.')
        logger.log_a_logxd('ERROR',
                           f'validate_text_encoding({kwargs}) - Some unsupported files were provided! This rule works '
                           f'only for txt files.')

    # print(f' ----- Scanning {len(kwargs["files"]["txt"])} txt files ------')
    logger.log_a_logxd('LOG',
                       f'validate_text_encoding({kwargs}) - Scanning {len(kwargs["files"]["txt"])} txt files')
    for txt_file in kwargs['files']['txt']:
        failed = 0
        for encoding in kwargs['encodings']:
            try:
                open(txt_file, mode='r', encoding=encoding).read()
                logger.log_a_logxd('LOG',
                                   f'validate_text_encoding({kwargs}) - {txt_file} has valid encoding - {encoding}')
            except Exception:
                failed += 1
        if failed == len(kwargs['encodings']):
            # print(f'File {txt_file} doesn\'t meet encoding requirements!')
            logger.log_a_logxd('ALERT',
                               f'validate_text_encoding({kwargs}) - {txt_file} does not meet encoding requirements!')


def validate_file_structure(**kwargs):
    if kwargs['files']['pcap'] or kwargs['files']['evtx'] or kwargs['files']['txt']:
        # print(f'Some unsupported files were provided! This rule works only for json and xml files.')
        logger.log_a_logxd('ERROR',
                           f'validate_file_structure({kwargs}) - Some unsupported files were provided! This rule works only for json and xml files.')
    # print(f' ----- Scanning {len(kwargs["files"]["json"])} json files -----')
    logger.log_a_logxd('LOG',
                       f'validate_file_structure({kwargs}) - Scanning {len(kwargs["files"]["json"])} json files')
    for json_file in kwargs['files']['json']:
        try:
            json.loads(open(json_file, 'r', encoding='utf-8-sig').read())
            logger.log_a_logxd('LOG',
                               f'validate_file_structure({kwargs}) - opened {json_file}')
        except Exception as e:
            print(f'{e}: {json_file}')
            logger.log_a_logxd('ERROR',
                               f'validate_file_structure({kwargs}) - unable to open {json_file}')
    # print(f' ----- Scanning {len(kwargs["files"]["xml"])} xml files ------')
    logger.log_a_logxd('LOG',
                       f'validate_file_structure({kwargs}) - Scanning {len(kwargs["files"]["json"])} xml files')

    for xml_file in kwargs['files']['xml']:
        try:
            parser = xml.sax.make_parser()
            parser.setContentHandler(xml.sax.ContentHandler())
            parser.parse(xml_file)
            logger.log_a_logxd('LOG',
                               f'validate_file_structure({kwargs}) - opened {xml_file}')
        except Exception as e:
            print(f'{e.args[0]} {xml_file}')
            logger.log_a_logxd('ERROR',
                               f'validate_file_structure({kwargs}) - unable to open {xml_file}')


def check_for_ip_address(**kwargs):
    r = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    # print(f' ----- Scanning {len(kwargs["files"]["pcap"])} pcap files -----')
    logger.log_a_logxd('LOG',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["pcap"])} pcap files')

    for pcap_file in kwargs['files']['pcap']:
        found_ip = []
        try:
            traffic = ps.FileCapture(pcap_file)
            for packet in traffic:
                if 'IP' in packet:
                    if packet['IP'].dst not in found_ip and packet['IP'].dst in kwargs['ip']:
                        # print(f'IP address {packet["IP"].dst} found in file {pcap_file}')
                        logger.log_a_logxd('LOG',
                                           f'check_for_ip_address({kwargs}) - IP address {packet["IP"].dst} found in file {pcap_file}')

                        found_ip.append(packet["IP"].dst)
                    if packet['IP'].src not in found_ip and packet['IP'].src in kwargs['ip']:
                        # print(f'IP address {packet["IP"].src} found in file {pcap_file}')
                        logger.log_a_logxd('LOG',
                                           f'check_for_ip_address({kwargs}) - IP address {packet["IP"].dst} found in file {pcap_file}')

                        found_ip.append(packet["IP"].src)
        except Exception:
            pass
    # print(f' ----- Scanning {len(kwargs["files"]["txt"])} txt files, {len(kwargs["files"]["json"])} json files and {len(kwargs["files"]["xml"])} xml files -----')
    logger.log_a_logxd('LOG',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["txt"])} txt files, {len(kwargs["files"]["json"])} json files and {len(kwargs["files"]["xml"])} xml files')

    for file in kwargs['files']['txt'] + kwargs['files']['json'] + kwargs['files']['xml']:
        try:
            text = open(file, mode='r').read()
            ip_list = list(dict.fromkeys(r.findall(text)))
            for ip in ip_list:
                if ip in kwargs['ip']:
                    # print(f'IP address {ip} found in file {file}')
                    logger.log_a_logxd('ALERT',
                                       f'check_for_ip_address({kwargs}) - IP address {ip} found in file {file}')

        except Exception:
            pass
    # print(f' ----- Scanning {len(kwargs["files"]["evtx"])} evtx files -----')
    logger.log_a_logxd('ALERT',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["evtx"])} evtx files')

    for evtx_file in kwargs['files']['evtx']:
        event = ''
        try:
            with evtx.Evtx(evtx_file) as event_log:
                for record in event_log.records():
                    for i in record.xml():
                        event += i
                ip_list = list(dict.fromkeys(r.findall(event)))
                for ip in ip_list:
                    if ip in kwargs['ip']:
                        # print(f'IP address {ip} found in file {evtx_file}')
                        logger.log_a_logxd('ALERT',
                                           f'check_for_ip_address({kwargs}) - IP address {ip} found in file {evtx_file}')

        except Exception as e:
            print(e)
            logger.log_a_logxd('ERROR',
                               f'check_for_ip_address({kwargs}) - Error with evtx files')

