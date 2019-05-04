import json
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

# Recursive with memorization
with open("performance_memo.json", "r") as f:
    memo = json.load(f)

plt.plot(memo, label="Recursion with memorization")

# Naive recursion
with open("performance_naive.json", "r") as f:
    naive = json.load(f)

plt.plot(naive, label="Naive recursion")

# Genetic algorithm
with open("performance_ga.json", "r") as f:
    ga = json.load(f)

plt.plot(ga, label="Genetic algorithm")

# plot stuff
plt.grid()
plt.title("Time taken to find solution")
plt.xlabel("Number of items")
plt.ylabel("Seconds")
plt.legend()
plt.savefig("performance.png")