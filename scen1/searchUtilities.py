import click
import os
import re

filenamePattern = "^[^\0\/]{1,250}\.(txt|py|xml|json)$"


@click.command()
@click.option('--file', '-f', default="", help='File to filter')
@click.option('--pattern', '-p', default="", help='Regular expression pattern, should be entered in ""')
def grep_via_grep(file, pattern):
    grep_via_x(file, pattern, 'grep')


@click.command()
@click.option('--file', '-f', help='File to filter')
@click.option('--pattern', '-p', help='Regular expression pattern, should be entered in ""')
def grep_via_re(file, pattern):
    grep_via_x(file, pattern, 're')


def grep_via_x(file, pattern, re_or_grep):
    validPath = re.match(filenamePattern, file)
    if not validPath:
        print("invalid file, only txt, py, xml, json extensions supported")
    elif not os.path.isfile(file):
        print("file not found")
    else:
        if re_or_grep == 're':
            with open(file) as f:
                for line in f:
                    if re.search(pattern, line):
                        print(line, end="")
        elif re_or_grep == 'grep':
            cmd = "cat " + file + " | grep -E \"" + pattern + "\""
            os.system(cmd)
