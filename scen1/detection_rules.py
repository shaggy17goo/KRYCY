import json
import re
import xml.sax
import pyshark as ps
import Evtx.Evtx as evtx
import requests
import alert_generator


def validate_text_encoding(**kwargs):
    for txt_file in kwargs['txt']:
        failed = 0
        for encoding in kwargs['encodings']:
            try: open(txt_file, mode='r', encoding=encoding).read()
            except: failed+=1
        if failed == len(kwargs['encodings']):
            alert_generator.alert(name='validate_text_encoding', content=f'File {txt_file} doesn\'t meet encoding requirements!')


def validate_file_structure(**kwargs):
    for json_file in kwargs['json']:
        try: json.loads(open(json_file, 'r', encoding='utf-8-sig').read())
        except Exception as e:
            alert_generator.alert(name='validate_file_structure', content=f'{e}: {json_file}')
    parser = xml.sax.make_parser()
    parser.setContentHandler(xml.sax.ContentHandler())
    for xml_file in kwargs['xml']:
        try: parser.parse(xml_file)
        except Exception as e:
            alert_generator.alert(name='validate_file_structure', content=f'{e.args[0]} {xml_file}')


def check_for_ip_address(**kwargs):
    r = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for pcap_file in kwargs['pcap']:
        found_ip = []
        try:
            traffic = ps.FileCapture(pcap_file)
            for packet in traffic:
                if 'IP' in packet:
                    for ip in [packet['IP'].dst, packet['IP'].src]:
                        if ip not in found_ip and ip in kwargs['ip']:
                            alert_generator.alert(name='check_for_ip_address', content=f'IP address {ip} found in file {pcap_file}')
                            found_ip.append(ip)
        except Exception: pass
    for file in kwargs['txt']+kwargs['json']+kwargs['xml']:
        try: 
            text = open(file, mode='r').read()
            ip_list = list(dict.fromkeys(r.findall(text)))
            for ip in ip_list:
                if ip in kwargs['ip']: 
                    alert_generator.alert(name='check_for_ip_address', content=f'IP address {ip} found in file {file}')
        except Exception: pass
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
                            alert_generator.alert(name='check_for_ip_address', content=f'IP address {ip} found in file {evtx_file}')
        except Exception: pass
