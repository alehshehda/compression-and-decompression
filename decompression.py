import time
import math as m


"""
FUNKCJA DLA DEKOMPRESJI PLIKU
1)WYCIAGAMY POTRZEBNE ZMIENNE Z PLIKU SKOMPRESOWANEGO(LICZBE UNIKALNYCH WARTOSCI,
POSORTOWANE WARTOSCI I ILOSC BITOW UZUPELNIAJACYCH) ORAZ DANE DLA DEKOMPRESJI
2)TWORZYMY SLOWNIK DLA DEKOMPRESJI PLIKU {BIN : CHAR}, WARTOSIC BIN ZAPISANE JAKO CHAR, WARTOSCI CHAR ZAPISANE
DO PLIKU ZRODLOWEGO JUZ POSORTOWANE OD NAJCZESTSZYCH 
3)Z KAZDEGO BAJTA WYCIAGAMY BITY I ZACHOWUJEMY W ZMIENNEJ BOOL_LIST
4)ZAMIENIAMY WARTOSCI BINARNE NA WARTOSCI BINARNE ZACHOWANE JAKO CHAR(DLA DZIALANIA SLOWNIKA)
5)OBCINAMY BITY UZUPELNIAJACE
6)WYCIAGAMY ODPOWIEDNIA ILOSC BITOW I ZAMIENAMY JE ZGODNIE ZE SLOWNIKIEM
7)ZAPIS WARTOSCI ZAMIENIONYCH DO PLIKU DOCELOWEGO
"""


def decompress(to_decompress_file, decompressed_file):
    # inicjalizowane czasu dla dekompresji
    start_time_decompression = time.time()

    # przeksztalcenie wartosci 10-ych do binarnych z okreslona dlugoscia
    def dec_to_bin(decimal, length):
        binary = bin(decimal)[2:]
        padded_binary = binary.zfill(length)
        return padded_binary

    # pobieramy liczby uniklanych wartosci, unikalnych wartosci oraz bitow uzupelniajacych
    with open(to_decompress_file, 'rb') as source:
        unique_chars = ord(source.read(1))  # liczba unikalnych wartosci
        bits_per_char = m.ceil(m.log(unique_chars, 2))  # ilosc bitow ktore potrzebne dla zapisu jednej wartosci
        sorted_char_list = [chr(byte) for byte in source.read(unique_chars)]  # wartosci, juz posortowane dla slownika
        padding_bits = ord(source.read(1))  # liczba bitow uzupelniajacych
        packed_data = source.read()  # dane dla dekompresji

    # tworzenie tablicy dla wartosci binarnych(zapisanych jako char)
    binary_list = list()
    for i in range(unique_chars):
        binary_list.append(dec_to_bin(i, bits_per_char))

    # tworzenie slownika {bin : char} (wartosci bin zapisane tez jako char)
    bin_to_char_dict = dict(zip(binary_list, sorted_char_list))

    # wyciagamy bajty do postaci bitow(0/1) do tablicy bool_list
    bool_list = []
    for byte in packed_data:
        for i in range(7, -1, -1):
            bool_list.append((byte >> i) & 1)

    # z wartosci int robimy wartosci char dla prawidlowego dzialania slownika
    char_bool_list = ['0' if x == 0 else '1' for x in bool_list]

    # obcinamy niepotrzebne bity
    if padding_bits != 0:
        char_bool_list = char_bool_list[:-padding_bits]

    # wyciagamy n bitow zapisanych jako char dla prawidlowego uzycia w slowniku
    # czyli porownanie odpowiednej liczby bin(zapisanych w postaci char) : char
    # bierzemy odpowiedna ilosc bitow dla dekompresji
    decompressed_data = list()
    for i in range(0, len(char_bool_list), bits_per_char):
        binary_to_decompress = ''.join(char_bool_list[i:i+bits_per_char])
        decompressed_data.append(bin_to_char_dict[binary_to_decompress])

    # zapis do pliku zdekompresowanego
    with open(decompressed_file, "w") as f:
        for value in decompressed_data:
            f.write(value)

    # podliczanie koncowego czasu wykonania dekompresji
    end_time_decompression = time.time()
    execution_time_decompression = end_time_decompression - start_time_decompression
    print("Time it takes to decompress: ", execution_time_decompression)
