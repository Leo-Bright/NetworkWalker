import json


def main(input_walk, node2segment_dict, output_walk):
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

    city = 'newyork'

    main(input_walk=city + '/network/' + city + '_random_wn10_wl1280.walks',
         node2segment_dict=city + '/dataset/' + city + '_nodes2segment.json',
         output_walk=city + '/network/' + city + '_random_wn10_wl1280.mixture')