from inspect import getmembers, isfunction
import sys

def list_rules(path):
    sys.path.append(path)
    import detection_rules
    i = 1
    for fun in getmembers(detection_rules, isfunction):
        print(f'{i}. {fun[0]}')
        i+=1
        #func = getattr(detection_rules, fun[0])
        #func()

list_rules('/home/mateusz/Desktop/rules')
