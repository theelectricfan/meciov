# models/vehicle.py

import numpy as np
from utils.ahp import compute_satisfaction_score
from config import BASE_BID_MULTIPLIER, BID_INCREMENT

class Vehicle:
    def __init__(self, id, task):
        self.id = id
        self.task = task
        self.bid_history = []
        self.assigned = False               # ✅ Add this
        self.assigned_sbs = None            # ✅ And this
        self.satisfaction = 0               # (set via AHP)


    def compute_base_bid(self, cpu_price, bw_price, metrics):
        # metrics = {'price': x, 'ber': y, 'retransmissions': z}
        satisfaction = compute_satisfaction_score(metrics)
        self.satisfaction = satisfaction

        # Base willingness to pay
        price = BASE_BID_MULTIPLIER * satisfaction * (
            cpu_price * self.task.cpu_cycles + bw_price * self.task.data_size
        )
        return price

    def generate_bid(self, round_number, cpu_price, bw_price, metrics):
        base = self.compute_base_bid(cpu_price, bw_price, metrics)
        bid = base * (BID_INCREMENT ** round_number)
        self.bid_history.append(bid)
        return bid
