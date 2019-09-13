#!/usr/bin/python
# -*- encoding: utf8 -*-

from tools import graph
import random
import json


__author__ = 'Leo'


def main(network_input="sanfrancisco/network/sf_roadnetwork",
         intersection_input="sanfrancisco/dataset/nodes_intersection.json",
         node_type_output="sanfrancisco/dataset/node_type.txt"):

    all_nodes = set()
    with open(network_input) as f:
        for line in f:
            source, target = line.strip().split(' ')
            all_nodes.add(source)
            all_nodes.add(target)

    with open(intersection_input) as f:
        intersection = json.loads(f.readline())

    def get_node_tyep(intersection, node):
        for (type, node_set) in intersection.items():
            if node in node_set:
                return type
        return '1'

    sorted_nodes = sorted(all_nodes)

    with open(node_type_output, 'w+') as f:
        for node in sorted_nodes:
            type = get_node_tyep(intersection, node)
            f.write(str(node) + ' ' + type + '\n')


main(network_input="seattle/network/seattle.network",
     intersection_input="seattle/dataset/seattle_intersection.json",
     node_type_output="seattle/dataset/node_type.seattle"
     )
