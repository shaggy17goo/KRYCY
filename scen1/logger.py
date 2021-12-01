import log as lg


def output(out, end='\n'):
    file = open("../data/blue_toolkit.log", "a")
    file.write(f"[CONSOLE OUTPUT]: {out} \n")
    file.close()
    print(out, end=end)


class Logger:
    def __init__(self, database):
        self.database = database

    def log_a_logxd(self, log_type, description, result=None, if_print=False):
        log = lg.Log(log_type, description, result)
        self.database.add_data(log)
        file = open("../data/blue_toolkit.log", "a")
        file.write(str(log) + "\n")
        if if_print:
            output(log)
