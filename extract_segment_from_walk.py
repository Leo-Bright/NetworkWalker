import json


def main(input_walk, node2segment_dict, segment_length, output):
    with open(node2segment_dict) as node2segment_file:
        node2segment_line = node2segment_file.readline()
        node2segment = json.loads(node2segment_line)
    segments_pair = set()
    for _, segments in get_segments(input_walk, node2segment):
        size = len(segments)
        for idx in range(size - 1):
            t1 = (segments[idx], segments[idx + 1])
            t2 = (segments[idx + 1], segments[idx])
            if t2 not in segments_pair:
                segments_pair.add(t1)

    length_dict = {}
    with open(segment_length) as length_file:
        for line in length_file:
            seg, len = line.strip().split(' ')
            length_dict[seg] = len

    with open(output, 'w+') as output_file:
        for item in segments_pair:
            (seg_start, seg_end) = item
            start_len = length_dict[seg_start]
            end_len = length_dict[seg_end]
            length = int(start_len) + int(end_len)
            output_file.write(seg_start + ' ' + seg_end + ' ' + str(length))


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

    main(input_walk='sanfrancisco/network/sf_random_wn10_wl1280.walks',
         node2segment_dict='sanfrancisco/network/sanfrancisco_nodes2segment.json',
         segment_length='sanfrancisco/network/sanfrancisco.length',
         output='sanfrancisco/network/sf_random_wn10_wl1280.segments',
         )
