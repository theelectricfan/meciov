# utils/knapsack.py

def multidimensional_knapsack(bids, cpu_cap, bw_cap):
    """
    Select the optimal set of bids to maximize revenue using a 2D knapsack approximation.
    Each bid = {'id': vehicle_id, 'price': val, 'cpu': GHz, 'bw': MHz}
    """
    bids = sorted(bids, key=lambda b: b['price'] / (b['cpu'] + b['bw']), reverse=True)
    selected = []
    total_cpu = total_bw = 0

    for bid in bids:
        if total_cpu + bid['cpu'] <= cpu_cap and total_bw + bid['bw'] <= bw_cap:
            selected.append(bid)
            total_cpu += bid['cpu']
            total_bw += bid['bw']

    return selected
