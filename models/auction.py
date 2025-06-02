import random
from config import MAX_AUCTION_ROUNDS
from utils.logger import CSVLogger

class AuctionController:
    def __init__(self, base_stations, vehicles, cpu_price=1e-3, bw_price=1e-5):
        self.base_stations = base_stations
        self.vehicles = vehicles
        self.cpu_price = cpu_price
        self.bw_price = bw_price
        self.rounds = MAX_AUCTION_ROUNDS
        self.unassigned = set([v.id for v in vehicles])
        self.logger = CSVLogger()

    def run(self):
        """
        Conducts multi-round auction until all vehicles are served or max rounds hit.
        """
        for round_num in range(self.rounds):
            print(f"\n🔁 Auction Round {round_num+1}")

            for v in self.vehicles:
                if v.id not in self.unassigned:
                    continue

                bs = random.choice(self.base_stations)

                # Dummy BER and retrans values — can be randomized or modeled
                metrics = {'price': 1, 'ber': 0.01, 'retrans': 1}
                bid_price = v.generate_bid(round_num, self.cpu_price, self.bw_price, metrics)

                bid = {
                    'id': v.id,
                    'price': bid_price,
                    'cpu': v.task.cpu_cycles / 1e9,  # GHz·s
                    'bw': v.task.data_size / 1e6,    # Mbit
                    'vehicle': v
                }

                bs.receive_bid(bid)

            # Evaluate and assign winners
            for bs in self.base_stations:
                winners = bs.run_auction_round()
                for winner in winners:
                    self.unassigned.discard(winner['id'])

            if not self.unassigned:
                print("✅ All vehicles assigned within", round_num + 1, "rounds.")
                break

        # ✅ Final Logging: only once per vehicle
        for v in self.vehicles:
            last_bid = v.bid_history[-1] if v.bid_history else 0

            tx_delay = v.task.data_size / (100 * 1e6) * 1000  # ms
            exec_delay = v.task.cpu_cycles / (10 * 1e9) * 1000  # ms
            total_delay = tx_delay + exec_delay

            self.logger.log(
                vehicle_id=v.id,
                round_num=self.rounds,
                bid_price=last_bid,
                assigned=v.assigned,
                sbs_id=v.assigned_sbs if v.assigned else -1,
                task_deadline_ms=v.task.deadline,
                total_delay_ms=total_delay,
                satisfaction_score=v.satisfaction
            )

        print(f"📊 {len(self.unassigned)} vehicles left unassigned after {self.rounds} rounds.")
