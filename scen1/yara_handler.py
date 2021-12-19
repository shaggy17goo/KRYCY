import os
import re
import yara

def simple_yara_validation(path):
    r1 = re.compile(r'^.+\.(yar)$')
    return r1.match(path)

def load_yara_rules(path, recursive):
    yara_rules = []
    r1 = re.compile(r'^.+\.(yml)$')
    r2 = re.compile(r'^(rule )')
    output_string = 'Found YARA rules:\n'
    i = 1
    if os.path.isfile(path):
        if (simple_yara_validation(path)):
            yara_rules.append(path)
            name = path[path.rfind('/')+1:]
            output_string+=f'{i}. {name}\n'
        else: 
            print("Not a YARA rule!")
    else:
        for root, dirs, files in os.walk(path):
            if root[-1] != '/':
                root += '/'
            for file in files:
                if (simple_yara_validation(root+file)):
                    yara_rules.append(root + file)
                    output_string+=f'{i}. {file}\n'
                    i += 1
            if not recursive: break
    print(output_string)
    return yara_rules
    
def yara_handler(path_to_rule, path_to_file):
    action_alert = 'remote'
    action_block = None
    description = ''
    rf = open(path_to_rule, 'r')
    rule = yara.compile(file=rf)
    rf.close()
    matches = rule.match(path_to_file)
    if matches:
        description += f'\nYARA rule {matches[0].rule} match file {path_to_file}:'
        for data in matches[0].strings:
            description += f'\n >Found {data[1]} string ({data[2]}) in file {path_to_file} (offset={data[0]})'
    else:
        action_alert = None
        description = None
    return action_alert, action_block, description
