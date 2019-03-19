import json


def main(input_walk, node2segment_dict, output_walk):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    for walk_line in input_walk:
        nodes = walk_line.strip().split(' ')
        if len(nodes) < 10:
            continue
        else:
            trans_node_to_segment(nodes)


def trans_node_to_segment(array):
    pass


if __name__ == '__main__':
    main('path/to/walk',
         'sanfrancisco/network/sanfrancisco_nodes2segment.json',
         'sanfrancisco/network/')