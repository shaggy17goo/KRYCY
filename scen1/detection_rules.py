import json
import re
import os
import xml.sax
import pyshark as ps
import Evtx.Evtx as evtx
import nest_asyncio

# list of encodings to validate for
# change according to your preferences
ENCODING_LIST = ['ascii', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8',
                 'utf_8_sig']


def validate_text_encoding(**kwargs):
    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    for txt_file in kwargs['txt']:
        failed = 0
        for encoding in ENCODING_LIST:
            try:
                open(txt_file, mode='r', encoding=encoding).read()
            except:
                failed += 1
        if failed == len(ENCODING_LIST):
            detection = True
            description += (f'validate_text_encoding: File {txt_file} doesn\'t meet encoding requirements!\n')

    if not detection:
        action_alert = None
        description = None

    return action_alert, action_block, description


def validate_file_structure(**kwargs):
    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    for json_file in kwargs['json']:
        try:
            json.loads(open(json_file, 'r', encoding='utf-8-sig').read())
        except Exception as e:
            detection = True
            description += (f'validate_file_structure: {e}: {json_file}\n')
    parser = xml.sax.make_parser()
    parser.setContentHandler(xml.sax.ContentHandler())
    for xml_file in kwargs['xml']:
        try:
            parser.parse(xml_file)
        except Exception as e:
            detection = True
            description += (f'validate_file_structure: {e.args[0]} {xml_file}\n')

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
        print(
            'Couldn\'t find file with list of IPs! \nIn order to use this rule, create such file named "list_of_ip" in the same directory as "detection_rules.py" file. \nInside this file write one IP each line.')
        return

    action_alert = 'remote'
    action_block = None
    description = ''
    detection = False

    r = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for pcap_file in kwargs['pcap']:
        found_ip = []
        try:
            traffic = ps.FileCapture(pcap_file)
            for packet in traffic:
                if 'IP' in packet:
                    for ip in [packet['IP'].dst, packet['IP'].src]:
                        if ip not in found_ip and ip in kwargs['ip']:
                            detection = True
                            description += (f'check_for_ip_address: IP address {ip} found in file {pcap_file}\n')
                            found_ip.append(ip)
        except Exception:
            pass
    for file in kwargs['txt'] + kwargs['json'] + kwargs['xml']:
        try:
            text = open(file, mode='r').read()
            ip_list = list(dict.fromkeys(r.findall(text)))
            for ip in ip_list:
                if ip in kwargs['ip']:
                    detection = True
                    description += (f'check_for_ip_address: IP address {ip} found in file {file}\n')
        except Exception:
            pass
    for evtx_file in kwargs['evtx']:
        event = ''
        try:
            with evtx.Evtx(evtx_file) as event_log:
                for record in event_log.records():
                    for i in record.xml():
                        event += i
                ip_list = list(dict.fromkeys(r.findall(event)))
                for ip in ip_list:
                    if ip in kwargs['ip']:
                        detection = True
                        description += (f'check_for_ip_address: IP address {ip} found in file {evtx_file}\n')
        except Exception:
            pass

    if not detection:
        action_alert = None
        description = None

    return action_alert, action_block, description