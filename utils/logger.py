# utils/logger.py

import csv
import os

class CSVLogger:
    def __init__(self, filename="results/auction_log.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(self.filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "vehicle_id", "round", "bid_price", "assigned", "sbs_id",
                "task_deadline_ms", "total_delay_ms", "satisfaction_score"
            ])

    def log(self, vehicle_id, round_num, bid_price, assigned, sbs_id,
            task_deadline_ms, total_delay_ms, satisfaction_score):
        with open(self.filename, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                vehicle_id, round_num, bid_price, assigned, sbs_id,
                task_deadline_ms, total_delay_ms, satisfaction_score
            ])
