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
         walk_num=2, num_process=1):

    print('Load a road Graph...')

    G = graph.load_edgelist(network_input, undirected=True)

    print('Generate random walks...')

    nodes = list(G.nodes())

    random.shuffle(nodes)

    G_nodes_size = len(nodes)

    print("Number of nodes: {}".format(G_nodes_size))

    num_walks = len(G.nodes()) * walk_num

    print("Total number of walks: {}".format(num_walks))

    print("Walking...")

    if num_process > 1:
        processes = []
        for i in range(num_process):
            start = int(G_nodes_size / num_process * i)
            end = int(G_nodes_size / num_process * (i + 1))
            if i == num_process - 1:
                end = G_nodes_size
            process_nodes = nodes[start:end]
            p = Process(target=walk_process,
                        args=(i, process_nodes, G, walk_num, walks_output))
            processes.append(p)

        for p in processes:
            p.start()
        for p in processes:
            p.join()
    else:
        process_nodes = nodes[:]
        walk_process(0, process_nodes, G, walk_num, walks_output)

    print("Merging results...")
    source_path, regex = walks_output.rsplit('/', 1)
    regex = regex + '_part'
    filename_list = get_filename_list(source_path, regex)
    filename_list.sort(key=lambda x: x.rsplit('.', 1)[1])

    for index, file in enumerate(filename_list):
        input_file_name = source_path + '/' + file
        input_file = open(input_file_name, 'r')
        if index == 0:
            with open(walks_output, 'w+') as output_file:
                shutil.copyfileobj(input_file, output_file)
        else:
            with open(walks_output, 'a') as output_file:
                shutil.copyfileobj(input_file, output_file)
        input_file.close()
        if os.path.exists(input_file_name):
            print("Deleting part file:", input_file_name)
            os.remove(input_file_name)



    print("Done!")


def get_filename_list(src_path, regex):
    import os
    result = []
    filenames = os.listdir(src_path)
    for file_name in filenames:
        if file_name.find(regex) >= 0:
            result.append(file_name)
    return result


def walk_process(pid, nodes, G, walk_num, output):

    output = output + '_part' + str(pid)

    nodes_in_process= len(nodes)

    everynode_walks = graph.build_shortest_path(G, nodes, num_paths=walk_num)

    with open(output, 'w+') as f:
        node_count = 0
        for node_walks in everynode_walks:
            for walk in node_walks:
                f.write('%s\n' % ' 0 '.join(map(str, walk)))
            node_count += 1
            if node_count % 50 == 0:
                ratio = float(node_count) / nodes_in_process
                sys.stdout.write(("\rPID <%d> walking ratio is :"
                                  "%d/%d (%.2f%%) "
                                  "" % (pid,
                                        node_count,
                                        nodes_in_process,
                                        ratio * 100,
                                        )))
                sys.stdout.flush()

    print("Walking done...")


main(network_input="sanfrancisco/network/sf_roadnetwork",
     walks_output="sanfrancisco/network/sf_shortest_path.walks",
     walk_num=100, num_process=2)

