import json


def main(node2segment_file, segment_type_file):
    with open(node2segment_file) as f:
        node2segment_dict = f.readline()
        node2segment = json.loads(node2segment_dict)

    segment_type = {}
    with open(segment_type_file) as f:
        for line in f:
            id_type = line.strip().split(' ')
            segment_type[id_type[0]] = id_type[1]

    for key in node2segment:
        _segments = node2segment[key]
        for k in _segments:
            road_segment = _segments[k]
            if str(road_segment) not in segment_type:
                raise Exception('there is no segment:', road_segment)


if __name__ == '__main__':
    main(node2segment_file='porto/network/porto_nodes2segment.json',
         segment_type_file='porto/network/segment_types.porto')