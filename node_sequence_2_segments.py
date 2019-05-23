import json


def main(input_walk, node2segment_dict, output_walk):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    with open(output_walk, 'w+') as f:
        for segments in get_segments(input_walk, node2segment):
            _segments = []
            pointer = 0
            for segment in segments:
                if pointer == 0:
                    _segments.append(segment)
                    pointer += 1
                elif _segments[pointer-1] != segment:
                    _segments.append(segment)
                    pointer += 1
            f.write('%s\n' % ' 0 '.join(map(str, _segments)))


def get_segments(input_walk, node2segment):
    with open(input_walk) as input_walk_file:
        for walk_line in input_walk_file:
            nodes = walk_line.strip().split(' ')
            if len(nodes) < 10:
                continue
            else:
                segments = trans_node_to_segment(nodes, node2segment)
                yield segments


def trans_node_to_segment(nodes, node2segment):
    segments = []
    last_node = None
    for node in nodes[::2]:
        if last_node is not None:
            _segment = node2segment[last_node]
            segment = _segment[node]
            segments.append(segment)
        last_node = node
    return segments


if __name__ == '__main__':
    main(input_walk='sanfrancisco/network/sf_random_wn10_wl1280.walks',
         node2segment_dict='sanfrancisco/network/sanfrancisco_nodes2segment.json',
         output_walk='sanfrancisco/network/sf_random_wn10_wl1280.segments')