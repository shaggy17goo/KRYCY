from datetime import datetime


class Log:
    def __init__(self, log_type, description):
        self.log_type = log_type
        self.description = description
        self.date = datetime.now()
