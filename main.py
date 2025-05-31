# main.py

from models.task import Task
from models.vehicle import Vehicle
from models.base_station import BaseStation
from models.auction import AuctionController
from config import NUM_VEHICLES, NUM_SBS, SBS_CPU_CAP, SBS_BW

import random

def init_vehicles():
    vehicles = []
    for i in range(NUM_VEHICLES):
        task = Task(i)
        vehicle = Vehicle(i, task)
        vehicles.append(vehicle)
    return vehicles

def init_base_stations():
    base_stations = []
    for i in range(NUM_SBS):
        bs = BaseStation(
            id=i,
            tier="SBS",
            cpu_capacity=SBS_CPU_CAP,
            bw_capacity=SBS_BW
        )
        base_stations.append(bs)
    return base_stations

def run_simulation():
    print("🚗 Initializing Vehicles and Tasks...")
    vehicles = init_vehicles()
    print(f"   → {len(vehicles)} vehicles initialized.")

    print("📡 Initializing SBS Nodes...")
    sbs_nodes = init_base_stations()
    print(f"   → {len(sbs_nodes)} SBS nodes initialized.")

    print("🏁 Starting Auction-Based Task Offloading...\n")
    auction = AuctionController(base_stations=sbs_nodes, vehicles=vehicles)
    auction.run()

    total_revenue = sum(bs.revenue for bs in sbs_nodes)
    total_assigned = sum(len(bs.assigned_tasks) for bs in sbs_nodes)

    print("\n📈 Final Results:")
    print(f"   → Total Revenue Collected by All SBSs: ₹{total_revenue:.2f}")
    print(f"   → Total Tasks Offloaded: {total_assigned} / {NUM_VEHICLES}")
    print(f"   → Success Rate: {100 * total_assigned / NUM_VEHICLES:.2f}%")

if __name__ == "__main__":
    run_simulation()
