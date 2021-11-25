import click

import pcap_parser as pp
import scanning_utilities as su
import search_utilities as search


@click.group()
def cli():
    pass


@cli.command()
@click.option('--rule-list', '-r', required=True, help='Path to directory with detection_rules.py file')
def listrules(rule_list):
    su.list_rules(rule_list)


@cli.command()
@click.option('--rule-list', '-l', required=True, help='Path to directory with detection_rules.py file')
@click.option('--rules', '-r',
              help='Comma separated numbers of rules to use (e.g. -r 1,3,4 ), by default all rules from file are used')
@click.option('--path', '-p', multiple=True, required=True, help='Path to file or directory to scan')
@click.option('--deep', '-d', is_flag=True, help='Scan files in subdirectories')
@click.option('--type', '-t', multiple=True,
              type=click.Choice(['txt', 'json', 'xml', 'pcap', 'evtx'], case_sensitive=True),
              help='File type to load. By deafult all types are loaded')
def scanfiles(rule_list, rules, path, deep, type):
    su.scan_files(rule_list, rules, path, deep, type)


@cli.command()
@click.option('--file', '-f', default="", help='File to filter')
@click.option('--pattern', '-p', default="", help='Regular expression pattern, should be entered in ""')
def grepViaGrep(file, pattern):
    search.grep_via_x(file, pattern, 'grep')


@cli.command()
@click.option('--file', '-f', help='File to filter')
@click.option('--pattern', '-p', help='Regular expression pattern, should be entered in ""')
def grepViaRe(file, pattern):
    search.grep_via_x(file, pattern, 're')


@cli.command()
@click.option('--path', '-p', prompt='Path to pcap file', help='Path for pcap file to view')
@click.option('--filter', '-f', default='', prompt='Display filter',
              help='Wireshark\'s display filter used for viewing PCAP file')
def printPcap(path, filter):
    pp.extract_traffic(path, filter)


cli.add_command(listrules)
cli.add_command(scanfiles)
cli.add_command(grepViaGrep)
cli.add_command(grepViaRe)
cli.add_command(printPcap)

if __name__ == '__main__':
    cli()

