import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys, os

args_len = 2

if len(sys.argv) < args_len + 1:
    print("require {} additional arguments".format(args_len-len(sys.argv)))
    print("python3 ./plotting.py <heap_size> <benchmark>")
    exit()


heap_size = sys.argv[1]
benchmarks = ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"]
benchmark = benchmarks[int(sys.argv[2])]
heuristics = ["qtable", "adaptive", "static", "compact", "aggressive"]
file_names = [os.path.join("Shenandoah", h, heap_size, benchmark + ".csv") for h in heuristics]

df = None
for file_name, heuristic in zip(file_names, heuristics):
    temp_df = pd.read_csv(file_name, sep=";", index_col="allocations", names=["allocations", heuristic], header=0)
    if df is None:
        df = temp_df
        continue
    df = pd.concat([df, temp_df], axis=1)

print(df)

df.plot(kind="line")
plt.show()