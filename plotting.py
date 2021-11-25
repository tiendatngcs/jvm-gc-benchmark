import numpy as np
import pandas as pd
import os
import re
from collections import defaultdict
from matplotlib import pyplot as plt


def plot_avg_runtime():
    all_heap_sizes = ['128', '256', '512']
    all_benchmarks = ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize']
    heuristics = ['qtable', 'adaptive', 'static', 'compact', 'aggressive']

    avg_runtime_df = pd.DataFrame({'benchmarks': ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize']})
    # parse files
    result_dict_128 = defaultdict(list)
    result_dict_256 = defaultdict(list)
    result_dict_512 = defaultdict(list)
    for size in all_heap_sizes:
        # calculate the avg runtime of each heuristic in each benchmark
        for benchmark in all_benchmarks:
            df = None
            for h in heuristics:
                file_name = (os.path.join('Shenandoah', h, size, benchmark + '.csv'))
                temp_df = pd.read_csv(file_name, sep=';', index_col='allocations', names=['allocations', h], header=0)
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
    plt.xticks(np.arange(len(all_benchmarks)), ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize'])
    plt.title('Runtime Average of Application with heapsize of 128')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 128.png')

    for key in result_dict_256.keys():
        avg_runtime_df[key] = result_dict_256[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize'])
    plt.title('Runtime Average of Application with heapsize of 256')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 256.png')

    for key in result_dict_512.keys():
        avg_runtime_df[key] = result_dict_512[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize'])
    plt.title('Runtime Average of Application with heapsize of 512')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 512.png')
    # plt.show()


def plot_mem_usage():
    pattern1 = re.compile('^capacity')
    pattern2 = re.compile('^used')
    heuristics = ['qtable', 'adaptive', 'static', 'compact', 'aggressive']
    result = defaultdict(list)
    for h in heuristics:
        if h == 'qtable':
            for file in os.listdir('log/'):
                if file.startswith("gc_ad"):
                    with open(os.path.join('log/', file), 'r') as f:
                        mem = 0
                        for line in f:
                            line = line.rstrip()
                            for match in re.finditer(pattern1, line):
                                temp = line.split(' ')
                                if temp[0] == '5':
                                    mem = 512
                                elif temp[0] == '2':
                                    mem = 256
                                else:
                                    mem = 128

                            for match in re.finditer(pattern2, line):
                                temp = line.split(' ')
                                result[mem].append(temp[1])
    print(result)

if __name__ == '__main__':
    # plot_avg_runtime()

    plot_mem_usage()