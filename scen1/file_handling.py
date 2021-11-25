import os
import re


def get_files(path_list, recursive, extensions=['pcap', 'evtx', 'json', 'xml', 'txt']):
    found_files = []
    for path in path_list:
        r = re.compile(r'^.+\.(pcap|evtx|json|xml|txt)$')
        if os.path.isfile(path):
            found_files.append(path)
        else:
            for root, dirs, files in os.walk(path):
                if root[-1] != '/':
                    root += '/'
                for file in files:
                    if (r.match(file)):
                        found_files.append(root + file)
                if not recursive: break
        filtered_files = {}
        for extension in {'pcap', 'evtx', 'json', 'xml', 'txt'}:
            filtered_files[extension] = []
        for extension in extensions:
            regex = '^.+\.{ext}$'.format(ext=extension)
            filtered_files[extension] = list(filter(re.compile(regex).match, found_files))
    return filtered_files
