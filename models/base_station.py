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
        valid_bids = []

        for bid in self.bids_received:
            task = bid['vehicle'].task
            cpu_demand = bid['cpu']  # in GHz·s
            data_size = bid['bw']    # in Mbit

            # Assume fixed resource frequency per SBS
            cpu_freq = 50.0  # GHz
            bandwidth = 1000.0  # Mbps

            # Delay estimations
            exec_delay_ms = (task.cpu_cycles / (cpu_freq * 1e9)) * 1000
            tx_delay_ms = (task.data_size / (bandwidth * 1e6)) * 1000
            total_delay_ms = exec_delay_ms + tx_delay_ms

            if total_delay_ms <= task.deadline:
                valid_bids.append(bid)
            else:
                print(f"⏱️ Rejected Vehicle {bid['id']} due to delay {total_delay_ms:.2f} ms > {task.deadline:.2f} ms")

        winners = multidimensional_knapsack(valid_bids, self.cpu_capacity, self.bw_capacity)
        self.assigned_tasks = winners
        for winner in winners:
            v = winner['vehicle']
            v.assigned = True
            v.assigned_sbs = self.id

        self.revenue = sum([b['price'] for b in winners])
        return winners

