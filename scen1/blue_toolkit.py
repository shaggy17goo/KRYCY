import click
import pcap_parser as pp
import scanning_utilities as su
import search_utilities as search
import yara_handler as yh
import threshold_detection as detection


@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', '-p', required=True, help='Path to directory with detection_rules.py file')
def list_python_rules(rule_list):
    su.list_rules(rule_list)

@cli.command()
@click.option('--rules', '-r', required=True, help='Path to direcory with yara rules / Path to single rule')
@click.option('--deep', '-d', is_flag=True, help='Search for rules in subdirectories')
def list_yara_rules(rules, deep):
    yh.load_yara_rules(rules, deep)

@cli.command()
@click.option('--rules', '-r', required=True, help='Path to directory with detection_rules.py file')
@click.option('--rule-selection', '-s',
              help='Comma separated numbers of rules to use (e.g. -r 1,3,4 ), by default all rules from file are used')
@click.option('--path', '-p', multiple=True, required=True, help='Path to file or directory to scan')
@click.option('--deep', '-d', is_flag=True, help='Scan files in subdirectories')
@click.option('--type', '-t', multiple=True,
              type=click.Choice(['txt', 'json', 'xml', 'pcap', 'evtx'], case_sensitive=True),
              help='File type to load. By deafult all types are loaded')
def scan_files_with_python_rules(rules, rule_selection, path, deep, type):
    su.scan_files_with_python_rules(rules, rule_selection, path, deep, type)

@cli.command()
@click.option('--rules', '-r', required=True, help='Path to directory with YARA rules / Path to single rule')
@click.option('--rules-deep', '-D', is_flag=True, help='Search for rules in subdirectories')
@click.option('--rule-selection', '-s',
              help='Comma separated numbers of rules to use (e.g. -r 1,3,4 ), by default all available rules from are used')
@click.option('--path', '-p', multiple=True, required=True, help='Path to file or directory to scan')
@click.option('--deep', '-d', is_flag=True, help='Scan files in subdirectories')
@click.option('--type', '-t', multiple=True,
              type=click.Choice(['txt', 'json', 'xml', 'evtx'], case_sensitive=True),
              help='File type to load. By deafult all types are loaded')
def scan_files_with_yara_rules(rules, rules_deep, rule_selection, path, deep, type):
    su.scan_files_with_yara_rules(rules, rules_deep, rule_selection, path, deep, type)

@cli.command()
@click.option('--file', '-f', default="", help='File to filter')
@click.option('--pattern', '-p', default="", help='Regular expression pattern, should be entered in ""')
def grep_via_grep(file, pattern):
    search.grep_via_x(file, pattern, 'grep')


@cli.command()
@click.option('--file', '-f', help='File to filter')
@click.option('--pattern', '-p', help='Regular expression pattern, should be entered in ""')
def grep_via_re(file, pattern):
    search.grep_via_x(file, pattern, 're')

@cli.command()
@click.option('--file', '-f', help='File with data in .csv')
@click.option('--type_of_detection', '-t', multiple=False,
              type=click.Choice(['flow_duration', 'unique_ports', 'high_difference'], case_sensitive=False))
def anomaly_detection(file, type_of_detection):
    detection.detection_click(file, type_of_detection)


@cli.command()
@click.option('--path', '-p', prompt='Path to pcap file', help='Path for pcap file to view')
@click.option('--filter', '-f', default='', prompt='Display filter',
              help='Wireshark\'s display filter used for viewing PCAP file')
def print_pcap(path, filter):
    pp.extract_traffic(path, filter)


cli.add_command(list_python_rules)
cli.add_command(list_yara_rules)
cli.add_command(scan_files_with_python_rules)
cli.add_command(scan_files_with_yara_rules)
cli.add_command(grep_via_grep)
cli.add_command(grep_via_re)
cli.add_command(print_pcap)
cli.add_command(anomaly_detection)

if __name__ == '__main__':
    cli()

