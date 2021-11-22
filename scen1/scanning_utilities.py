import alert_generator
import sys
import re
import os

from inspect import getmembers, isfunction

def list_rules(rule_list):
    sys.path.append(rule_list)
    try:
        import detection_rules
        print('Detection rules in provided file:')
        i = 1
        for fun in getmembers(detection_rules, isfunction):
            print(f'{i}. {fun[0]}')
            i+=1
    except Exception as e:
        print(e)


def scan_files(rule_list, rules, path, deep, type):
    if rules:
        rules = rules.replace(' ', '')
        rules = rules.split(',')
    if len(type) == 0:
        extensions=['json','xml', 'pcap', 'txt']
    else: 
        extensions=list(type)
    loaded_files = get_files(list(path), deep, extensions)
    sys.path.append(rule_list)
    try:
        import detection_rules
        number_of_rule = 0
        for rule in getmembers(detection_rules, isfunction):
            number_of_rule += 1
            if rules and (str(number_of_rule) not in rules):
                continue
            print(f'--------------------------------------------\n> Using rule: {rule[0]}')
            func = getattr(detection_rules, rule[0])
            action_alert, action_block, description = func(pcap=loaded_files['pcap'], json=loaded_files['json'], xml=loaded_files['xml'], txt=loaded_files['txt'], evtx=loaded_files['evtx'])
            if description:
                alert_generator.alert(name=rule[0], content=description, remote=(action_alert=='remote'))
            else:
                print('No alerts returned.')
    except Exception as e:
        print(e)


def get_files(path_list, recursive, extensions=['pcap', 'evtx', 'json', 'xml', 'txt']):
    found_files = []
    for path in path_list:
        r = re.compile(r'^.+\.(pcap|evtx|json|xml|txt)$')
        if os.path.isfile(path):
            found_files.append(path)
        else:
            for root, dirs, files in os.walk(path):
                if root[-1]!='/':
                    root+='/'
                for file in files:
                    if(r.match(file)):
                        found_files.append(root + file)
                if not recursive: break
        filtered_files = {}
        print('Files loaded for analysis:')
        for extension in {'pcap', 'evtx', 'json', 'xml', 'txt'}:
            if extension in extensions:
                regex = '^.+\.{ext}$'.format(ext = extension)
                filtered_files[extension] = list(filter(re.compile(regex).match, found_files))
            else: 
                filtered_files[extension] = []
            print(f'{extension}:{len(filtered_files[extension])}  ', end='')
        print('\n')    
    return filtered_files