import json
import random
import sys
import time

sys.setrecursionlimit(2500)

memo = {}
def ks(capacity_left, n):
    """
        capacity_left(int): remaining storage capacity of a bag
        n(int): current item position
    """

    if n == -1 or capacity_left == 0:
        # No more items to add
        return 0
    
    # h = hash("%d_%d" % (capacity_left, n))

    h = capacity_left * 2000 + n

    if h in memo:
        # print("memo", capacity_left, n)
        return memo[h]

    if weights[n] > capacity_left:
        # Current item is too heavy for remaining capacity, ignore it and continue
        return ks(capacity_left, n-1)
    else:
        # Do not add item, just move the pointer to the left
        _without = ks(capacity_left, n-1)
        # Add item into bag
        _with = values[n] + ks(capacity_left-weights[n], n-1)
        
        # Save value into memory
        val = max(_with, _without)
        memo[h] = val

        return val

weights = []
values = []
capacities = []
bests = []

capacity = 0

for i in range(2001):
    begin = time.time()
    
    weights.append(random.randint(0, 100))
    values.append(random.randint(0, 100))
    capacity += random.randint(0, 25)

    capacities.append(capacity)

    best = ks(capacity, len(weights)-1)
    bests.append(best)

    memo = {}

    end = time.time()
    seconds = end - begin
    print("Items", i)
    # print(weights)
    # print(values)
    print("Capacity:", capacity)
    print("Best:", best)
    print("Seconds:", seconds)
    print("*"*40)

    with open("dataset.json", "w+") as f:
        ds = {
            "values": values,
            "weights": weights,
            "capacities": capacities,
            "bests": bests
        }

        json.dump(ds, f, indent=4)