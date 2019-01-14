#!/usr/bin/python
# -*- encoding: utf8 -*-

from tools import graph
import random
import sys
from multiprocessing import Process
import shutil
import os

__author__ = 'Leo'


def main(network_input="sanfrancisco/network/sf_roadnetwork",
         walks_output="res/sf_roadnetwork.walks",
         num_process=1):

    print('Load a road Graph...')

    G = graph.load_edgelist(network_input, undirected=True)

    print('Generate random walks...')

    nodes = list(G.nodes())

    random.shuffle(nodes)

    G_nodes_size = len(nodes)

    print("Number of nodes: {}".format(G_nodes_size))

    num_walks = len(G.nodes()) * 320

    print("Total number of walks: {}".format(num_walks))

    print("Walking...")

    if num_process > 1:
        processes = []
        for i in range(num_process):
            start = int(G_nodes_size / num_process * i)
            end = int(G_nodes_size / num_process * (i + 1))
            if i == num_process - 1:
                end = G_nodes_size
            p = Process(target=walk_process,
                        args=(i, nodes, start, end, G, walks_output))
            processes.append(p)

        for p in processes:
            p.start()
        for p in processes:
            p.join()
    else:
        walk_process(0, nodes, 0, G_nodes_size, G, walks_output)

    print("Merging results...")
    # regex_40 = regex + '_40_part'
    # regex_80 = regex + '_80_part'
    # regex_160 = regex + '_160_part'
    # regex_320 = regex + '_320_part'
    regex_list = ['_40', '_80', '_160', '_320']
    source_path, regex = walks_output.rsplit('/', 1)

    for str in regex_list:
        _regex = regex + str
        filename_list = get_filename_list(source_path, _regex)
        filename_list.sort(key=lambda x: x.rsplit('.', 1)[1])

        for index, file in enumerate(filename_list):
            input_file_name = source_path + '/' + file
            input_file = open(input_file_name, 'r')
            if index == 0:
                with open(walks_output + str, 'w+') as output_file:
                    shutil.copyfileobj(input_file, output_file)
            else:
                with open(walks_output + str, 'a') as output_file:
                    shutil.copyfileobj(input_file, output_file)
            input_file.close()
            if os.path.exists(input_file_name):
                print("Deleting part file:", input_file_name)
                os.remove(input_file_name)
    print("Done!")


def get_filename_list(src_path, regex):
    import os
    result = []
    file_names = os.listdir(src_path)
    for file_name in file_names:
        if file_name.find(regex) >= 0:
            result.append(file_name)
    return result


def walk_process(pid, nodes, start, end, G, output):

    output_40 = output + '_40_part' + str(pid)
    output_80 = output + '_80_part' + str(pid)
    output_160 = output + '_160_part' + str(pid)
    output_320 = output + '_320_part' + str(pid)

    nodes_count_in_process = end - start

    every_node_walks = graph.build_shortest_path(G, nodes, start, end)

    node_count = 0
    for node_walks in every_node_walks:
        with open(output_40, 'w+') as f:
            for walk in node_walks['40']:
                f.write('%s\n' % ' 0 '.join(map(str, walk)))
        with open(output_80, 'w+') as f:
            for walk in node_walks['80']:
                f.write('%s\n' % ' 0 '.join(map(str, walk)))
        with open(output_160, 'w+') as f:
            for walk in node_walks['160']:
                f.write('%s\n' % ' 0 '.join(map(str, walk)))
        with open(output_320, 'w+') as f:
            for walk in node_walks['320']:
                f.write('%s\n' % ' 0 '.join(map(str, walk)))
        node_count += 1
        if node_count % 50 == 0:
            ratio = float(node_count) / nodes_count_in_process
            sys.stdout.write(("\rPID <%d> walking ratio is :"
                              "%d/%d (%.2f%%) "
                              "" % (pid,
                                    node_count,
                                    nodes_count_in_process,
                                    ratio * 100,
                                    )))
            sys.stdout.flush()

    print("Walking done...")


main(network_input="sanfrancisco/network/sanfrancisco.network",
     walks_output="sanfrancisco/network/sanfrancisco.walks",
     num_process=44)

