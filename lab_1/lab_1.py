import random
import os
import struct
import array
import time


def generate_random_array(size):
    return [random.randint(1, 1000000) for _ in range(size)]


def write_array_to_file(file_path, array):
    with open(file_path, 'wb') as file:
        array.tofile(file)


def read_array_from_file(file_path, array_typecode):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)
        element_size = struct.calcsize(array_typecode)
        array_size = file_size // element_size
        file_content = array.array(array_typecode)
        file_content.fromfile(file, array_size)
        return file_content


def sort_array_in_memory(array):
    array.sort()


def sort_large_array_in_chunks(file_path, chunk_size):
    temp_file_path = 'temp_sorted_file.bin'
    with open(file_path, 'rb') as file:
        try:
            while True:
                chunk = array.array('q')
                chunk.fromfile(file, chunk_size)
                if not chunk:
                    break
                chunk = array.array('q', sorted(chunk))
                with open(temp_file_path, 'ab') as temp_file:
                    chunk.tofile(temp_file)
        except EOFError as err:
            print(err)
    os.replace(temp_file_path, file_path)


def main():
    # Part 1: Sort small array in memory
    small_array_size = 10000000
    small_array = generate_random_array(small_array_size)
    sort_array_in_memory(small_array)

    # Write and read small array to/from file
    file_path_small = 'small_array.bin'
    write_array_to_file(file_path_small, array.array('q', small_array))
    print('finished small array')
    small_array_from_file = read_array_from_file(file_path_small, 'q')

    # Part 2: Sort large array in chunks
    # large_array_size = 1000000000  # 1 GB
    large_array_size = 100000000  # 1 GB
    large_array = generate_random_array(large_array_size)

    # Write large array to file
    file_path_large = 'large_array.bin'
    start_time = time.time()
    write_array_to_file(file_path_large, array.array('q', large_array))
    end_time = time.time()
    print(end_time - start_time)

    # Sort large array in chunks
    start_time = time.time()
    sort_large_array_in_chunks(file_path_large, chunk_size=10000000)  # 100MB chunks
    end_time = time.time()

    print(f'Sorting time for large array: {end_time - start_time} seconds')


if __name__ == '__main__':
    main()
