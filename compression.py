import math
import time
import struct
import sys
from collections import Counter
from encryption import encrypt_message


def dec_to_bin(decimal, length):
    """
    Funkcja przeksztalca wartosci base10 do base2 z okreslona dlugoscia bitow
    :param decimal: wartosc base 10
    :param length: okreslona dlugosc dla base2
    :return: zwraca wartosc base2 bez pomijana zer wodzacych(np. 0010)
    """
    binary = bin(decimal)[2:]
    padded_binary = binary.zfill(length)
    return padded_binary

def compress(to_compress_file, compressed_file, public_key):
    """
    FUNKCJA DLA KOMPRESJI PLIKU
    :param to_compress_file: plik zawartosc ktorego zostanie skompresowana
    :param compressed_file: plik w ktorym skompresowana wartosc zostanie umieszczona
    :param public_key: klucz publiczny ktory zostanie wykorzystany dla szyfrowania informacji
    :return execution_time_compression: zwraca ile czasu zajela kompresja

    1)Inicjalizacja potrzebnych zmiennych
    2)Tworzenie tablicy unikalnych wartosci posortowanych od najczestszych
    3)Szyfrowanie tablicy zawierajacyh unikalne wartosci i pobieranie jej dlugosci
    4)Tworzenie tablicy ktora zawiera w sobie wartosci base2 w postaci char
    5)Tworzenie slownika {char: bin}, wartosci posortowane od najczestszych, wartosci 'bin' zapisane w postaci char
    6)Zapis do pliku bitow uzupelniajacych, zasyfrowane unikalne wartosci(krok 3) oraz zapis dlugosci informacji z kroku 3
    7)Tworzenie zmiennej dla zachowana wartosci jedno-bitowych i zapelnienie jej za pomoca slownika z kroku 5
    8)Dodawanie padding_bits jezeli sa do zmiennej z kroku 7
    9)Tworzenie zmiennej ktora bedzie zachowywac 8 wartosci(bajt) na raz ze zmiennej wartosci z kroku 7,
      zapis bit po bicie tych wartosci
    10)Zwracanie calkowitego czasu wykonania kompresji pliku
    """

    # inicjalizowanie czasu dla kompresji
    start_time_compression = time.time()

    # pobieranie zawartosci pliku zrodlowego
    with open(to_compress_file, "r") as f:
        plain_text = f.read()

    # inicjalizjowane niezbednych zmiennych
    total_chars = len(plain_text)  # ilosc wszystkich znakow
    unique_chars = len(list(set(plain_text)))  # ilosc unikalnych znakow
    bits_per_char = math.ceil(math.log(unique_chars, 2))  # potrzebne bity do zapisania jednej skompresowanej wartosci
    padding_bits = (8 - (total_chars * bits_per_char) % 8) % 8  # ilosc bitow uzupelniajacych


    # sortowanie wartosci wedlug ilosci wystapien w tekscie, robimy z tego tablice
    char_count = Counter(plain_text)
    char_frequency_list = [(char, count) for char, count in char_count.items()]
    sorted_char_frequency = sorted(char_frequency_list, key=lambda x: x[1], reverse=True)
    sorted_char_list = [char for char, _ in sorted_char_frequency]

    # szyfrowanie tablicy zawierajacyh uniklane wartosci i obliczamy jej dlugosc
    sorted_char_list_encrypted = encrypt_message(''.join(sorted_char_list), public_key)
    size_of_ecnrypted_char = len(sorted_char_list_encrypted)

    # tworzenie tablicy z wartosciami base2 w postaci char
    binary_list = list()
    for i in range(unique_chars):
        binary_list.append(dec_to_bin(i, bits_per_char))

    # tworzenie slownika {char : bin} (wartosci bin zapisane tez jako char)
    char_to_bin_dict = dict(zip(sorted_char_list, binary_list))

    # zapis wartosci do pliku skompresowanego
    with open(compressed_file, "wb") as destination:

        # zapisujemy padding bits, zasyfrowane unikalne wartosci i dlugosc ktora zajmuja zaszyfrowane unikalne wartosci
        destination.write(chr(padding_bits).encode())
        destination.write(struct.pack('I', len(sorted_char_list_encrypted)))
        destination.write(sorted_char_list_encrypted)

        list_of_bools = list()  # lista bedzie zawierac wartosci jedno-bitowe
        # przeksztalcenie wartosci binarnych char w rzeczywiste jedno-bitowe wartosci
        try:
            for char in plain_text:
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
