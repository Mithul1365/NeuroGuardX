import csv
import os
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(
    BASE_DIR,
    "..",
    "logs",
    "driver_log.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "..",
    "logs",
    "Risk_Graph.png"
)


class GraphGenerator:

    @staticmethod
    def generate():

        if not os.path.exists(LOG_FILE):
            print("driver_log.csv not found")
            return

        time_data = []
        risk_data = []

        with open(LOG_FILE, newline="") as file:

            reader = csv.DictReader(file)

            for i, row in enumerate(reader):

              if i % 20 != 0:
                continue

              time_data.append(i)

              risk_data.append(float(row["Risk"]))
        plt.figure(figsize=(9, 5))

        plt.plot(
            time_data,
            risk_data,
            color="red",
            linewidth=2,
            marker="o",
            markersize=4,
            label="Risk Score"
        )

        plt.title(
            "NeuroGuard X - Driver Risk Analysis",
            fontsize=14,
            fontweight="bold"
        )

        plt.xlabel("Log Entries")

        plt.ylabel("Risk Score (%)")

        plt.ylim(0, 100)

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            OUTPUT_FILE,
            dpi=300
        )

        plt.close()

        print("Risk Graph Saved :", OUTPUT_FILE)