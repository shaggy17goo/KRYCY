import scanning_utilities as su
import click


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


cli.add_command(listrules)
cli.add_command(scanfiles)

if __name__ == '__main__':
    cli()

# tutaj najlpiej doklejcie swoje clickowe metody

# wtedy bedzie wszystko sie bedzie wykonywalo np "python blue_toolkit.py scanfiles --i-opcje-tutaj"
# i fajnego helpa sie dostaje przy okazji

#
#   [osboxes@osboxes scen1]$ python blue_toolkit.py 
#   Usage: blue_toolkit.py [OPTIONS] COMMAND [ARGS]...
#
#   Options:
#       --help  Show this message and exit.
#
#   Commands:
#       listrules
#       scanfiles


# bo teraz jak sie prosto z konsoli wykonuje z tym setup.py entry points to nawet nie wiadomo co nasz program moze robic
# nazwa pliku oczywscie do zmiany jak cos xd
