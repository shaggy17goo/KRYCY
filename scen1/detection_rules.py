import json
import re
import os
import xml.sax
import pyshark as ps
import Evtx.Evtx as evtx
import nest_asyncio
from database import Database
from logger import Logger


# list of encodings to validate for
# change according to your preferences
ENCODING_LIST = ['ascii', 'utf_32', 'utf_32_be', 'utf_32_le','utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']


db = Database()
logger = Logger(db)


def validate_text_encoding(**kwargs):
    if kwargs['pcap'] or kwargs'evtx'] or kwargs['json'] or kwargs['xml']:
        # print(f'Some unsupported files were provided! This rule works only for txt files.')
        logger.log_a_logxd('ERROR',
                           f'validate_text_encoding({kwargs}) - Some unsupported files were provided! This rule works '
                           f'only for txt files.')
    logger.log_a_logxd('LOG',f'validate_text_encoding({kwargs}) - Scanning {len(kwargs["files"]["txt"])} txt files')
    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    for txt_file in kwargs['txt']:
        failed = 0
        for encoding in ENCODING_LIST:
            try:
                open(txt_file, mode='r', encoding=encoding).read()
                logger.log_a_logxd('LOG',
                                   f'validate_text_encoding({kwargs}) - {txt_file} has valid encoding - {encoding}')
except:
                failed+=1
        if failed == len(ENCODING_LIST):
            detection = True
            description+=(f'validate_text_encoding: File {txt_file} doesn\'t meet encoding requirements!\n')
            logger.log_a_logxd('ALERT',
                               f'validate_text_encoding({kwargs}) - {txt_file} does not meet encoding requirements!')

if not detection:
        action_alert = None
        description = None

    return action_alert, action_block, description


def validate_file_structure(**kwargs):
    if kwargs['files']['pcap'] or kwargs['files']['evtx'] or kwargs['files']['txt']:
        # print(f'Some unsupported files were provided! This rule works only for json and xml files.')
        logger.log_a_logxd('ERROR',
                           f'validate_file_structure({kwargs}) - Some unsupported files were provided! This rule works only for json and xml files.')

    logger.log_a_logxd('LOG',
                       f'validate_file_structure({kwargs}) - Scanning {len(kwargs["files"]["json"])} json files')
    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    for json_file in kwargs['json']:
        try:
            json.loads(open(json_file, 'r', encoding='utf-8-sig').read())
            logger.log_a_logxd('LOG',
                               f'validate_file_structure({kwargs}) - opened {json_file}')
        except Exception as e:
            detection = True
            description+=(f'validate_file_structure: {e}: {json_file}\n')
            logger.log_a_logxd('ERROR',
                               f'validate_file_structure({kwargs}) - unable to open {json_file}')

    logger.log_a_logxd('LOG',
                       f'validate_file_structure({kwargs}) - Scanning {len(kwargs["files"]["xml"])} xml files')
    parser = xml.sax.make_parser()
    parser.setContentHandler(xml.sax.ContentHandler())
    for xml_file in kwargs['xml']:
        try:
            parser.parse(xml_file)
            logger.log_a_logxd('LOG',
                               f'validate_file_structure({kwargs}) - opened {xml_file}')
        except Exception as e:
            detection = True
            description+=(f'validate_file_structure: {e.args[0]} {xml_file}\n')
            logger.log_a_logxd('ERROR',
                               f'validate_file_structure({kwargs}) - unable to open {xml_file}')

    if not detection:
        action_alert = None
        description = None

    return action_alert, action_block, description


def check_for_ip_address(**kwargs):

    nest_asyncio.apply()
    dirname = os.path.dirname(__file__)
    full_path = os.path.join(dirname, 'list_of_ip')
    try:
        blacklist_ip = open(full_path, 'r')
        print(f'Scanning for IPs: {blacklist_ip.readlines()}')
    except:
        print('Couldn\'t find file with list of IPs! \nIn order to use this rule, create such file named "list_of_ip" in the same directory as "detection_rules.py" file. \nInside this file write one IP each line.')
        return

    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    r = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    logger.log_a_logxd('LOG',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["pcap"])} pcap files')
    for pcap_file in kwargs['pcap']:
        found_ip = []
        try:
            traffic = ps.FileCapture(pcap_file)
            for packet in traffic:
                if 'IP' in packet:
                    for ip in [packet['IP'].dst, packet['IP'].src]:
                        if ip not in found_ip and ip in kwargs['ip']:
                            detection = True
                            description+=(f'check_for_ip_address: IP address {ip} found in file {pcap_file}\n')
                            found_ip.append(ip)
                            logger.log_a_logxd('ALERT',
                                               f'check_for_ip_address({kwargs}) - IP address {ip} found in file {pcap_file}')

        except Exception:
            pass
    logger.log_a_logxd('LOG',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["txt"])} txt files, {len(kwargs["files"]["json"])} json files and {len(kwargs["files"]["xml"])} xml files')
    for file in kwargs['txt']+kwargs['json']+kwargs['xml']:
        try: 
            text = open(file, mode='r').read()
            ip_list = list(dict.fromkeys(r.findall(text)))
            for ip in ip_list:
                if ip in kwargs['ip']:
                    detection = True
                    description+=(f'check_for_ip_address: IP address {ip} found in file {file}\n')
                    logger.log_a_logxd('ALERT',
                                       f'check_for_ip_address({kwargs}) - IP address {ip} found in file {file}')

        except Exception:
            pass

    logger.log_a_logxd('LOG',
                       f'check_for_ip_address({kwargs}) - Scanning {len(kwargs["files"]["evtx"])} evtx files')

    for evtx_file in kwargs['evtx']:
        event = ''
        try:
            with evtx.Evtx(evtx_file) as event_log:
                for record in event_log.records():
                    for i in record.xml():
                        event+=i
                ip_list = list(dict.fromkeys(r.findall(event)))
                for ip in ip_list:
                        if ip in kwargs['ip']:
                            detection = True
                            description+=(f'check_for_ip_address: IP address {ip} found in file {evtx_file}\n')
                            logger.log_a_logxd('ALERT',f'check_for_ip_address({kwargs}) - IP address {ip} found in file {evtx_file}')

        except Exception:
            logger.log_a_logxd('ERROR',
                               f'check_for_ip_address({kwargs}) - Error with evtx files')

    if not detection:
        action_alert = None
        description = None

    return action_alert, action_block, description
