from compression import compress
from decompression import decompress
import os


def is_valid_file(file_path):
    return os.path.isfile(file_path)


def has_txt_extension(file_name):
    if not file_name.endswith('.txt'):
        return file_name + '.txt'
    return file_name


if __name__ == '__main__':

    # Kompresja
    to_compress_file = input("Please, enter the name of the file to be compressed: ")
    to_compress_file = has_txt_extension(to_compress_file)
    while not is_valid_file(to_compress_file):
        print("Error: Please enter a valid file name.")
        to_compress_file = input("Please, enter the name of the file to be compressed: ")

    compressed_file = input("Please, enter the name of the file to store compressed data: ")
    compressed_file = has_txt_extension(compressed_file)

    compress(to_compress_file, compressed_file)

    # Dekompresja
    to_decompress_file = input("Please, enter the name of the file to be decompressed: ")
    to_decompress_file = has_txt_extension(to_decompress_file)
    while not is_valid_file(to_decompress_file):
        print("Error: Please enter a valid file name.")
        to_decompress_file = input("Please, enter the name of the file to be decompressed: ")

    decompressed_file = input("Please, enter the name of the file to store decompressed data: ")
    decompressed_file = has_txt_extension(decompressed_file)

    decompress(to_decompress_file, decompressed_file)
