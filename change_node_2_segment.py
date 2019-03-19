import json


def main(input_walk, node2segment_dict, output_walk):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    with open(output_walk, 'w+') as f:
        for segments in get_segments(input_walk, node2segment):
            f.write('%s\n' % ' 0 '.join(map(str, segments)))


def get_segments(input_walk, node2segment):
    for walk_line in input_walk:
        nodes = walk_line.strip().split(' ')
        if len(nodes) < 10:
            continue
        else:
            segments = trans_node_to_segment(nodes, node2segment)
            yield segments


def trans_node_to_segment(nodes, node2segment):
    segments = []
    last_node = None
    for node in nodes:
        if last_node is not None:
            segment = node2segment[last_node][node]
            segments.append(segment)
        last_node = node
    return segments


if __name__ == '__main__':
    main('path/to/walk',
         'sanfrancisco/network/sanfrancisco_nodes2segment.json',
         'sanfrancisco/network/')