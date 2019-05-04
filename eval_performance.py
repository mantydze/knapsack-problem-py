from naive_recursive import ks as ks_naive
from memo_recursive import ks as ks_memo
from genetic_algorithm import KS as GA

import json
import time

results = [] # time taken, index is number of items

algorithm = "ga"

with open("dataset.json", "r") as f:
    data = json.load(f)

for n in range(1, 800):

    w = data["weights"][:n]
    v = data["values"][:n]
    c = data["capacities"][n-1]
    expected = data["bests"][n-1]

    start = time.time()

    if algorithm == "ga":
        
        # This is a hack because first two best values are zeros
        if n < 5:
            continue

        ga = GA(pop_size=1000, n_generations=100)
        ga.optimize(w, v, c, expected=expected)

    elif algorithm == "naive":
        best = ks_naive(c, n-1, w, v)
        if best != expected:
            print("Naive best != expected", best, expected)
            break

    elif algorithm == "memo":
        best = ks_memo(c, n-1, w, v, True)
        
        if best != expected:
            print("Memo best != expected", best, expected)
            break

    end = time.time()
    t = round(end-start, 1)

    print(n, " ",t, "sec")

    results.append(t)

    with open("performance_%s.json" % algorithm, "w+") as f:
        json.dump(results, f)
