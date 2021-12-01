import os
import re
import sys
import logger as lg
from inspect import getmembers, isfunction

import alert_generator
from database import Database
from logger import Logger

db = Database()
logger = Logger(db)


def list_rules(rule_list):
    logger.log_a_logxd('LOG', f'list_rules({rule_list})')
    sys.path.append(rule_list)
    try:
        import detection_rules
        lg.output('Detection rules in provided file:')
        i = 1
        for fun in getmembers(detection_rules, isfunction):
            lg.output(f'{i}. {fun[0]}')
            i += 1
    except Exception as e:
        lg.output(e)
        logger.log_a_logxd('ERROR', f'list_rules({rule_list}) failed')


def scan_files(rule_list, rules, path, deep, type):
    lg.output(f'scan_files({rule_list}, {rules}, {path}, {deep}, {type})')
    logger.log_a_logxd('LOG', f'scan_files({rule_list}, {rules}, {path}, {deep}, {type})')
    if rules:
        rules = rules.replace(' ', '')
        rules = rules.split(',')
    if len(type) == 0:
        extensions = ['json', 'xml', 'pcap', 'evtx', 'txt']
    else:
        extensions = list(type)
    loaded_files = get_files(list(path), deep, extensions)
    sys.path.append(rule_list)
    try:
        import detection_rules
        number_of_rule = 0
        for rule in getmembers(detection_rules, isfunction):
            number_of_rule += 1
            if rules and (str(number_of_rule) not in rules):
                continue
            lg.output(f'--------------------------------------------\n> Using rule: {rule[0]}')
            logger.log_a_logxd('LOG', f'scan_files({rule_list}, {rules}, {path}, {deep}, {type}) using rule {rule[0]}')
            func = getattr(detection_rules, rule[0])
            action_alert, action_block, description = func(pcap=loaded_files['pcap'], json=loaded_files['json'],
                                                           xml=loaded_files['xml'], txt=loaded_files['txt'],
                                                           evtx=loaded_files['evtx'])
            if description:
                logger.log_a_logxd('ALERT',
                                   f'scan_files({rule_list}, {rules}, {path}, {deep}, {type}) - {description}')
                alert_generator.alert(name=rule[0], content=description, remote=(action_alert == 'remote'))
                if action_block is not None:
                    alert_generator.block(action_block)
            else:
                logger.log_a_logxd('LOG',
                                   f'scan_files({rule_list}, {rules}, {path}, {deep}, {type}) - no alerts returned ')
                lg.output('No alerts returned.')
    except Exception as e:
        lg.output(e)


def get_files(path_list, recursive, extensions=['pcap', 'evtx', 'json', 'xml', 'txt']):
    found_files = []
    logger.log_a_logxd('LOG',
                       f'get_files({path_list}, {recursive}, {extensions})')
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
        lg.output('Files loaded for analysis:')
        logger.log_a_logxd('LOG',
                           f'get_files({path_list}, {recursive}, {extensions}) - Files loaded for analysis')
        for extension in {'pcap', 'evtx', 'json', 'xml', 'txt'}:
            if extension in extensions:
                regex = '^.+\.{ext}$'.format(ext=extension)
                filtered_files[extension] = list(filter(re.compile(regex).match, found_files))
            else:
                filtered_files[extension] = []
            lg.output(f'{extension}:{len(filtered_files[extension])}  ', end='')
        lg.output('\n')
    return filtered_files
