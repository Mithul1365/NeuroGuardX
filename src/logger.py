import csv
import os
from datetime import datetime


class DriverLogger:

    def __init__(self):

        os.makedirs("../logs", exist_ok=True)

        self.filename = "../logs/driver_log.csv"

        if not os.path.exists(self.filename):

            with open(self.filename, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Time",
                    "EAR",
                    "Head",
                    "Yawn",
                    "Face",
                    "Attention",
                    "Risk",
                    "Status"
                ])

    def log(
        self,
        ear,
        head,
        yawn,
        face,
        attention,
        risk,
        status
    ):

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%H:%M:%S"),
                round(ear, 2),
                head,
                yawn,
                face,
                attention,
                risk,
                status
            ])