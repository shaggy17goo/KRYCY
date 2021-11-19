from posixpath import join
from typing_extensions import Required
import detection_rules as dr
import file_handling as gf
import nest_asyncio
import click
    
nest_asyncio.apply() # bez tego się wysypuje na przeglądaniu wielu pcapow 

encodings_list = ['ascii', 'utf_32', 'utf_32_be', 'utf_32_le','utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']

@click.command()
@click.option('--recursive', '-r', is_flag=True, help='Load files from subdirectories')
@click.option('--path', '-p', multiple=True, required=True, help='Path to file or directory')
@click.option('--type', '-t', multiple=True, type=click.Choice(['txt', 'json', 'xml', 'pcap', 'evtx'], case_sensitive=True), help='File type to load. By deafult all types are loaded')
#@click.option('--check-for-ip', is_flag=True)
#@click.option('--ip-list', help='Path to file with IP addresses to load (one IP each line)')
#@click.option('--single-ip', help='Single IP to load')
#@click.option('--validate-structure', is_flag=True, help='Validate file structure (json/xml)')
#@click.option('--validate-encoding', is_flag=True, help='Validate encoding of files [ascii, utf_32, utf_32_be, utf_32_le, utf_16, utf_16_be, utf_16_le, utf_7, utf_8, utf_8_sig]')
def scan_files(recursive, path, type, check_for_ip, validate_structure, validate_encoding, ip_list, single_ip):
    if len(type) == 0:
        extensions=['json','xml', 'pcap', 'txt']
    else: 
        extensions=list(type)
    loaded_files = gf.get_files(list(path), recursive, extensions)
    if check_for_ip:
        loaded_ip = []
        if ip_list:
            try:
                loaded_ip = open(ip_list, 'r').read().splitlines()
                print(f'Loaded IPs {loaded_ip}')
            except Exception: pass
        elif single_ip: 
            print('got single ip')
            loaded_ip.append(single_ip)
        else: 
            print('In order to run this scan you have to provide IP address (or path to file with multiple IP addresses)')
            return
        dr.check_for_ip_address(pcap=loaded_files['pcap'], json=loaded_files['json'], xml=loaded_files['pcap'], txt=loaded_files['txt'], evtx=loaded_files['evtx'], ip=['51.83.134.233', '10.0.2.5', '213.127.65.23'])
    if validate_structure:
        dr.validate_file_structure(xml=loaded_files['xml'], json=loaded_files['json'])
    if validate_encoding:
        dr.validate_text_encoding(txt=loaded_files['txt'], encodings=encodings_list)

# TODO ogarnac podawanie ip i kodowania + cos na konsole wypisywac
