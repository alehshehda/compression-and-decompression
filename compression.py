import math as m
from collections import Counter
import time
import struct
import sys


"""
FUNKCJA DLA KOMPRESJI PLIKU 
1)INICJALIZACJA NIEZBEDNYCH ZMIENNYCH
2)TWORZENIE SLOWNIKA {CHAR : BIN}, WARTOSCI CHAR POSORTOWANE OD NAJCZESTSZYCH, WARTOSCI BIN ZAPISANE JAKO CHAR
3)ZAPIS DO PLIKU HEADER'A ZAWIERAJACEGO LICZBE UNIKALNYCH WARTOSCI, UNIKALNE WARTOSCI POSORTOWANE, BITY UZUPELNIAJACE
4)TWORZENIE ZMIENNEJ DLA ZACHOWANIA WARTOSCI TYPU BOOL(1 BITOWE)
5)PRZEKSZTALCENIE WARTOSCI BINARNYCH CHAR DO WARTOSCI BOOL
6)ZAPIS WARTOSCI TYPU BOOL DO PLIKU DOCELOWEGO BIT PO BICE
7)ZWRACA CZAS WYKONYWANIA KOMPRESJI PLIKU
"""


def compress(to_compress_file, compressed_file):
    # inicjalizowanie czasu dla kompresji
    start_time_compression = time.time()

    # pobieranie zawartosci pliku zrodlowego
    with open(to_compress_file, "r") as f:
        plain_text = f.read()

    # inicjalizjowane niezbednych zmiennych
    total_chars = len(plain_text)  # ilosc wszystkich znakow
    unique_chars = len(list(set(plain_text)))  # ilosc unikalnych znakow
    bits_per_char = m.ceil(m.log(unique_chars, 2))  # potrzebne bity do zapisania jednej skompresowanej wartosci
    padding_bits = (8 - (total_chars * bits_per_char) % 8) % 8  # ilosc bitow uzupelniajacych

    # przeksztalcenie wartosci 10-ych do binarnych z okreslona dlugoscia
    def dec_2_bin(decimal, length):
        binary = bin(decimal)[2:]
        padded_binary = binary.zfill(length)
        return padded_binary

    # sortowanie wartosci wedlug ilosci wystapien w tekscie
    char_count = Counter(plain_text)
    char_frequency_list = [(char, count) for char, count in char_count.items()]
    sorted_char_frequency = sorted(char_frequency_list, key=lambda x: x[1], reverse=True)
    sorted_char_list = [char for char, _ in sorted_char_frequency]

    # tworzenie tablicy z wartosciami binarnymi w postaci char
    binary_list = list()
    for i in range(unique_chars):
        binary_list.append(dec_2_bin(i, bits_per_char))

    # tworzenie slownika {char : bin} (wartosci bin zapisane tez jako char)
    char_to_bin_dict = dict(zip(sorted_char_list, binary_list))

    # zapis wartosci do pliku compressed.txt
    with open(compressed_file, "wb") as destination:

        # zapisywanie liczby unikalnych wartosci, wartosci slownika
        # oraz liczbe bitow uzupelniajacych
        header = chr(unique_chars) + ''.join(sorted_char_list) + chr(padding_bits)
        destination.write(header.encode("utf-8"))

        list_of_bools = list()  # lista bedzie zawierac wartosci bool
        # przeksztalcenie wartosci binarnych char w rzeczywiste jednobiotwe wartosci(bool)
        try:
            for char in plain_text:
                if char in char_to_bin_dict:
                    bin_value = char_to_bin_dict[char]
                    for bin_value_to_bool in bin_value:
                        if bin_value_to_bool == '1':
                            list_of_bools.append(True)
                        elif bin_value_to_bool == '0':
                            list_of_bools.append(False)
                        else:
                            print("Error with the dictionary")
                            sys.exit(1)

            # dodawanie bitow uzupelniajacyh
            if padding_bits != 0:
                for i in range(padding_bits):
                    list_of_bools.append(False)
        except Exception as e:
            print("Error, probably with the file.", e)

        # zmienna zachowuje po 8 bitow w jednej komorce
        bytes = [list_of_bools[i:i + 8] for i in range(0, len(list_of_bools), 8)]

        # zapis bit po bicie do pliku
        for byte in bytes:
            packed_bytes = 0
            for i, bit in enumerate(byte):
                packed_bytes |= bit << (7 - i)
            destination.write(struct.pack('B', packed_bytes))

    # podliczanie koncowego czasu wykonania kompresji
    end_time_compression = time.time()
    execution_time_compression = end_time_compression - start_time_compression
    return execution_time_compression
