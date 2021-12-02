import numpy as np
import math
import pandas as pd
import os
import re
from collections import defaultdict
from matplotlib import pyplot as plt
from numpy.core.arrayprint import printoptions
from numpy.core.fromnumeric import mean


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
    plt.title('Runtime Average of Application with heapsize of 128 MB')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 128 MB.png')

    for key in result_dict_256.keys():
        avg_runtime_df[key] = result_dict_256[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize'])
    plt.title('Runtime Average of Application with heapsize of 256 MB')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 256 MB.png')

    for key in result_dict_512.keys():
        avg_runtime_df[key] = result_dict_512[key]
    avg_runtime_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Application Runtime in Milliseconds')
    plt.xlabel('Benchmarks')
    plt.xticks(np.arange(len(all_benchmarks)), ['SingleCoreFixedSize', 'SingleCoreVaryingSize', 'MultipleCoresFixedSize', 'MultipleCoresVaryingSize'])
    plt.title('Runtime Average of Application with heapsize of 512 MB')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Runtime Average 512 MB.png')


def plot_mem_helper(filename):
    pattern = re.compile('^used')
    results = defaultdict(list)
    for file in os.listdir('log/'):
        if file.startswith(filename):
            mem = int(file[6:9])
            with open(os.path.join('log/', file), 'r') as f:
                for line in f:
                    line = line.rstrip()
                    for match in re.finditer(pattern, line):
                        temp = line.split(' ')
                        results[mem].append(int(temp[1]))
    for key in results.keys():
        results[key] = math.ceil(np.mean(results[key])) / 1000000 # round up to MB
    return results


def plot_mem_usage():
    heuristics = ['qtable', 'adaptive', 'static', 'compact', 'aggressive']
    qt_results = defaultdict(list)
    ad_results = defaultdict(list)
    ag_results = defaultdict(list)
    cp_results = defaultdict(list)
    st_results = defaultdict(list)
    for h in heuristics:
        if h == 'qtable':
            qt_results = plot_mem_helper('gc_qt')
        elif h == 'adaptive':
            ad_results = plot_mem_helper('gc_ad')
        elif h == 'static':
            st_results = plot_mem_helper('gc_st')
        elif h == 'compact':
            cp_results = plot_mem_helper('gc_cp')
        elif h == 'aggressive':
            ag_results = plot_mem_helper('gc_ag')
    
    avg_mem_df = pd.DataFrame({'sizes': ['128', '256', '512']})
    for h in heuristics:
        if h == 'qtable':
            avg_mem_df[h] = qt_results.values()
        elif h == 'adaptive':
            avg_mem_df[h] = ad_results.values()
        elif h == 'static':
            avg_mem_df[h] = st_results.values()
        elif h == 'compact':
            avg_mem_df[h] = cp_results.values()
        elif h == 'aggressive':
            avg_mem_df[h] = ag_results.values()
    print(avg_mem_df.head())
    avg_mem_df.plot.bar(rot=0)
    figure = plt.gcf()
    plt.ylabel('Average Memory Usage of Application in MB')
    plt.xlabel('Heap Sizes')
    plt.xticks(np.arange(3), ['128', '256', '512'])
    plt.title('Average Memory Usage of Applications')
    figure.set_size_inches(12, 9)
    plt.savefig('plot/Memory Usage Average.png')

if __name__ == '__main__':
    # plot_avg_runtime()

    plot_mem_usage()
