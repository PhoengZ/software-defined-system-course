import time
l = [0 for _ in range(50001)]
for i in range(50001):
    l[i] = time.perf_counter_ns()
base = l[0]
for i in range(50001):
    l[i] = (l[i] - base)*(10**-9)
with open("result.txt", "w") as f:
    for idx, val in enumerate(l):
        f.write(f"{idx}, {val:.8f}")
        f.write("\n")
