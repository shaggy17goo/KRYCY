import os
import re

#DEBUGGING
def grepViaRe(path, regexp):
    filenamePattern = "^[^\0\/]{1,250}\.(txt|py|xml|json)$"
    validPath = re.match(filenamePattern, path)
    if not validPath:
        print("invalid filed, only txt, py, xml, json supported")
    elif not os.path.isfile(path):
        print("file not found")
    else:
        with open(path) as f:
            for line in f:
                if re.search(regexp, line):
                    print(line, end="")

def grepViaGrep(file, pattern):
    filenamePattern = "^[^\0\/]{1,250}\.(txt|py|xml|json)$"
    validPath = re.match(filenamePattern, file)
    if not validPath:
        print("invalid file, only txt, py, xml, json extensions supported")
    elif not os.path.isfile(file):
        print("file not found")
    else:
        cmd = "cat " + file + " | grep -E \"" + pattern + "\""
        os.system(cmd)

if __name__ == '__main__':
    grepViaRe("searchUtilities.py", "click")


    print("\n\n\n")

    grepViaGrep("searchUtilities.py", "([A-W][a-w]{3}\s)")