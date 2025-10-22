import os
from datetime import datetime

class Setup:
    def __init__(self, file):
        self.path = "storage/logs"
        self.filename = f"{self.path}/{file}.log"
        self._prepareLogger()

    def _prepareLogger(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("DATE LEVEL MESSAGE\n")

    def write(self, level: str, message: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"{now} {level.upper()} {message}\n"

        with open(self.filename, "a") as f:
            f.write(log)
