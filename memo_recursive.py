"""
Knapsack problem.

Naive recursive implementation. Try all combinations (Bad idea)
Complexity is exponential (2^n) where n is number of items.

"""
# Uncomment the following lines if you want to play around with more than 2000 items
# import sys
# sys.setrecursionlimit(2500)

memo = {}
def ks(capacity_left, n, weights, values, clear_memo=False):
    """
        capacity_left (int): remaining storage capacity of a bag
        n (int): current item position
        weights (list): list of item weights
        values (list): list of item values
        clear_memo: used for performance tests only
    """

    if clear_memo:
        memo.clear()

    if n == -1 or capacity_left == 0:
        # No more items to add
        return 0
    
    h = capacity_left * 2000 + n
    if h in memo:
        # print("memo", capacity_left, n)
        return memo[h]

    if weights[n] > capacity_left:
        # Current item is too heavy for remaining capacity, ignore it and continue
        return ks(capacity_left, n-1, weights, values)
    else:
        # Do not add item, just move the pointer to the left
        _without = ks(capacity_left, n-1, weights, values)
        # Add item into bag
        _with = values[n] + ks(capacity_left-weights[n], n-1, weights, values)
        
        # Save value into memory
        val = max(_with, _without)
        memo[h] = val

        return val

if __name__ == "__main__":

    import json

    with open("dataset.json", "r") as f:
        data = json.load(f)

    n = 25
    w = data["weights"][:n]
    v = data["values"][:n]
    c = data["capacities"][n]

    best = ks(c, n-1, w, v)

    print("Best: ", best, "| Expected:", data["bests"][n])
