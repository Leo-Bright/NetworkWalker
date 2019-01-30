import os
import shutil


# get names of files in the directory
def get_filename_list(src_path, regex):
    import os
    result = []
    filenames = os.listdir(src_path)
    for file_name in filenames:
        if file_name.find(regex) >= 0:
            result.append(file_name)
    return result


def main(source_random, source_shortest, output_filename):

    # filename_list = get_filename_list(source_path, regex)
    # filename_list.sort(key=lambda x: x.rsplit('.', 1)[1])

    output_file = open(output_filename, 'a')

    random_file = open(source_random, 'r')
    shutil.copyfileobj(random_file, output_file)
    random_file.close()

    shortest_file = open(source_shortest, 'r')
    shutil.copyfileobj(shortest_file, output_file)
    shortest_file.close()

    output_file.close()


main(source_random='sanfrancisco/network/sf_random_wn10_wl1280.walks',
     source_shortest='sanfrancisco/network/sanfrancisco_shortest_distance.walks_80',
     output_filename='sanfrancisco/network/sf_random_shortest_wl1280_wn80.walks',
     )