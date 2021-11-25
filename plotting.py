from collections import defaultdict
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os


def plot_avg_runtime():
    all_heap_sizes = ['128', '256', '512']
    all_benchmarks = ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"]
    heuristics = ["qtable", "adaptive", "static", "compact", "aggressive"]

    avg_runtime_df = pd.DataFrame({'benchmarks': ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"]})
    # parse files
    result_dict_128 = defaultdict(list)
    result_dict_256 = defaultdict(list)
    result_dict_512 = defaultdict(list)
    for size in all_heap_sizes:
        # calculate the avg runtime of each heuristic in each benchmark
        for benchmark in all_benchmarks:
            df = None
            for h in heuristics:
                file_name = (os.path.join("Shenandoah", h, size, benchmark + ".csv"))
                temp_df = pd.read_csv(file_name, sep=";", index_col="allocations", names=["allocations", h], header=0)
                df = pd.concat([df, temp_df], axis=1)
            mean = df.mean().values.tolist()
            for index, value in enumerate(mean):
                if size == '128':
                    result_dict_128[heuristics[index]].append(value)
                elif size == '256':
                    result_dict_256[heuristics[index]].append(value)
                else:
                    result_dict_512[heuristics[index]].append(value)

    for key in result_dict_128.keys():
        avg_runtime_df[key] = result_dict_128[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"])
    plt.title('Runtime Average of Application with heapsize of 128')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 128.png')

    for key in result_dict_256.keys():
        avg_runtime_df[key] = result_dict_256[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"])
    plt.title('Runtime Average of Application with heapsize of 256')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 256.png')

    for key in result_dict_512.keys():
        avg_runtime_df[key] = result_dict_512[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ["SingleCoreFixedSize", "SingleCoreVaryingSize", "MultipleCoresFixedSize", "MultipleCoresVaryingSize"])
    plt.title('Runtime Average of Application with heapsize of 512')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 512.png')
    # plt.show()


def plot_mem_usage():
    pass

if __name__ == '__main__':
    plot_avg_runtime()