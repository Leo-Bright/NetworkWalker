import os
import json
import shutil
import numpy as np
from numpy import float16


def combine_embeddings(embeddings_list, method):
    matrix = np.array(embeddings_list, dtype=float16)
    if method == '+':
        result = matrix.sum(axis=0)
    elif method == '*':
        result = np.ones(len(matrix[0]))

        # matrix = np.abs(matrix)
        # matrix = np.log(matrix)
        # matrix = np.abs(matrix)
        # result = matrix.sum(axis=0)

        for i in range(matrix.shape[0]):
            result *= matrix[i]
        return result
    elif method == '&':
        result = np.append(matrix[0], matrix[-1])
    elif method == '-':
        col_size = matrix.shape[0]
        result = matrix.sum(axis=0)/col_size
    else:
        raise Exception
    return result.tolist()


def run(road_segments_file, node_embeddings_file, segment_embeddings_file, method):

    # filename_list = get_filename_list(source_path, regex)
    # filename_list.sort(key=lambda x: x.rsplit('.', 1)[1])
    with open(road_segments_file) as f:
        road_segments = json.loads(f.readline())

    node_embeddings = {}

    with open(node_embeddings_file, 'r') as f:
        for line in f:
            line = line.strip()
            osmid_vector = line.split(' ')
            osmid, node_vec = osmid_vector[0], osmid_vector[1:]
            if len(node_vec) < 10:
                continue
            node_embeddings[osmid] = node_vec

    error_segments = 0
    with open(segment_embeddings_file, 'w+') as f:
        for key in road_segments:
            segment = road_segments[key]
            source_node = segment['source']
            target_node = segment['target']
            try:
                source_node_embedding = node_embeddings[str(source_node)]
                target_node_embedding = node_embeddings[str(target_node)]
                segment_embedding = combine_embeddings([source_node_embedding, target_node_embedding], method)
                f.write(key + ' %s\n' % ' '.join(map(str, segment_embedding)))
            except:
                print("this segment encounter error:", key, source_node, target_node)
                error_segments += 1
        print("How many segments can not find embedding:", error_segments)


if __name__ == '__main__':

    run(road_segments_file='sanfrancisco/dataset/all_road_segments_dict.sanfrancisco',
        node_embeddings_file='../linearSVC/sanfrancisco/embedding/deepwalk/sf.embedding128',
        segment_embeddings_file='../linearSVC/sanfrancisco/embedding/deepwalk/sf_deepwalk_segment_128_multi.embedding',
        method='*',
        )
