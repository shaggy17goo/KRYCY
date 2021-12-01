from datetime import datetime


class Log:
    def __init__(self, log_type, description, result=None):
        self.log_type = log_type
        if result is not None:
            description = f"DESCRIPTION: \n {description} \n RESULT: \n {result}"
        self.description = description
        self.date = datetime.now()

    def __str__(self):
        return f"[{self.log_type}]  {self.date}  {self.description}"
