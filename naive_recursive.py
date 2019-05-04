"""
Knapsack problem.

Naive recursive implementation. Try all combinations (Bad idea)
Complexity is exponential (2^n) where n is number of items.

"""

def ks(capacity_left, n, weights, values):
    """
        capacity_left (int): remaining storage capacity of a bag
        n (int): current item position
        weights (list): list of item weights
        values (list): list of item values
    """

    if n == -1 or capacity_left == 0:
        # No more items to add
        return 0
    elif weights[n] > capacity_left:
        # Current item is too heavy for remaining capacity, ignore it and continue
        return ks(capacity_left, n-1, weights, values)
    else:
        # Do not add item, just move the pointer to the left
        _without = ks(capacity_left, n-1, weights, values)
        # Add item into bag
        _with = values[n] + ks(capacity_left-weights[n], n-1, weights, values)

        return max(_with, _without)

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
