import pyshark as ps
import click

@click.command()
@click.option('--path', '-p', prompt='Path to pcap file', help='Path for pcap file to view')
@click.option('--filter', '-f', default='', prompt='Display filter', help='Wireshark\'s display filter used for viewing PCAP file' )

def extract_traffic(path, filter):
    traffic = ps.FileCapture(path, display_filter=filter)
    print_traffic(traffic)

def print_traffic(traffic):
    for pcap in traffic:
        print(pcap)

if __name__ == '__main__':
    extract_traffic()
