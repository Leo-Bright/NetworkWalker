def split_mixture_embeddings(mixture_embedding_file, word_type_file, output_node_embedding_file, output_segment_embedding_file):

    node_set = set()
    with open(word_type_file) as f:
        for line in f:
            word_type = line.strip().split()
            word, type = word_type[0], word_type[1]
            if type == '0' or type == 0:
                node_set.add(word)

    output_node_embedding = open(output_node_embedding_file, 'w+')

    output_segment_embedding = open(output_segment_embedding_file, 'w+')

    with open(mixture_embedding_file) as f:
        for line in f:
            osmid_embeddings = line.strip().split(' ')
            if len(osmid_embeddings) < 10: continue
            osmid = osmid_embeddings[0]
            if osmid in node_set:
                output_node_embedding.write(line)
            else:
                output_segment_embedding.write(line)


if __name__ == '__main__':

    split_mixture_embeddings(mixture_embedding_file='sanfrancisco/embeddings/deepwalk/sf.mixture',
                             word_type_file='sanfrancisco/dataset/sf_word.type',
                             output_node_embedding_file='sanfrancisco/embeddings/deepwalk/sf_node.embedding',
                             output_segment_embedding_file='sanfrancisco/embeddings/deepwalk/sf_segment.embedding',
                             )
