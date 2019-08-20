import json


def node_sequence_2_segment_sequence(input_walk, node2segment_dict, output_walk):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    with open(output_walk, 'w+') as f:
        for _, segments in get_segments(input_walk, node2segment):
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


def node_sequence_2_mixture_sequence(input_walk, node2segment_dict, output_walk):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    with open(output_walk, 'w+') as f:
        for real_nodes, segments in get_segments(input_walk, node2segment):
            _mixtures = []
            assert len(real_nodes)-1 == len(segments)
            for idx in range(len(segments)):
                _mixtures.append(real_nodes[idx])
                _mixtures.append(segments[idx])
            _mixtures.append(real_nodes[-1])
            f.write('%s\n' % ' 0 '.join(map(str, _mixtures)))


def get_segments(input_walk, node2segment):
    with open(input_walk) as input_walk_file:
        for walk_line in input_walk_file:
            nodes = walk_line.strip().split(' ')
            if len(nodes) < 10:
                continue
            else:
                real_nodes, segments = trans_node_to_segment(nodes, node2segment)
                yield real_nodes, segments


def trans_node_to_segment(nodes, node2segment):
    segments = []
    real_nodes = []
    last_node = None
    for node in nodes[::2]:
        real_nodes.append(node)
        if last_node is not None:
            _segment = node2segment[last_node]
            segment = _segment[node]
            segments.append(segment)
        last_node = node
    return real_nodes, segments


if __name__ == '__main__':
    # node_sequence_2_segment_sequence(input_walk='sanfrancisco/network/sf_random_wn10_wl1280.walks',
    #                                  node2segment_dict='sanfrancisco/network/sanfrancisco_nodes2segment.json',
    #                                  output_walk='sanfrancisco/network/sf_random_wn10_wl1280.segments')

    node_sequence_2_mixture_sequence(input_walk='sanfrancisco/network/sf_random_wn10_wl1280.walks',
                                     node2segment_dict='sanfrancisco/network/sanfrancisco_nodes2segment.json',
                                     output_walk='sanfrancisco/network/sf_random_wn10_wl1280.mixture')