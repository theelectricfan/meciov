# models/task.py

import random

class Task:
    def __init__(self, id):
        self.id = id
        self.data_size = random.uniform(5, 20) * 8 * 1e6  # Convert MB to bits
        self.cpu_cycles = random.uniform(0.2e9, 1.0e9)
        self.deadline = random.uniform(500, 3000)  # in ms → 0.5s to 3s

