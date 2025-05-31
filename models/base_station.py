# models/base_station.py

from utils.knapsack import multidimensional_knapsack

class BaseStation:
    def __init__(self, id, tier, cpu_capacity, bw_capacity):
        self.id = id
        self.tier = tier  # 'SBS', 'MBS', 'CORE'
        self.cpu_capacity = cpu_capacity
        self.bw_capacity = bw_capacity
        self.bids_received = []
        self.assigned_tasks = []
        self.revenue = 0

    def receive_bid(self, bid):
        self.bids_received.append(bid)

    def clear_bids(self):
        self.bids_received.clear()
        self.assigned_tasks.clear()
        self.revenue = 0

    def run_auction_round(self):
        """
        Process all received bids using the knapsack selection.
        Each bid: {id, price, cpu, bw}
        """
        winners = multidimensional_knapsack(self.bids_received, self.cpu_capacity, self.bw_capacity)
        self.assigned_tasks = winners
        self.revenue = sum([b['price'] for b in winners])
        return winners
