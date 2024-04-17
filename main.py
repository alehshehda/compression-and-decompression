import math as m
from collections import Counter
import time
import struct


# LOGIKA DLA KOMPRESJI PLIKU


# inicjalizowawnie czasu dla kompresji
start_time_compression = time.time()

# definicja plikow zrodlowych i docelowych
to_compress_file = "to_compress.txt"
compressed_file = "compressed.txt"
uncompressed_file = "decompressed.txt"


# pobieranie zawartosci pliku zrodlowego
with open(to_compress_file, "r") as f:
    plain_text = f.read()

# inicjalizjowane niezbednych zmiennych
k = len(plain_text)  # ilosc wszystkich znakow
u = len(list(set(plain_text)))  # ilosc unikalnych znakow
n = m.ceil(m.log(u, 2))  # ilosc bitow ktorych potrzebujemy do zapisania jednej wartosci
r = (8 - (k * n) % 8) % 8  # ilosc bitow uzupelniajacych


# przeksztalcenie wartosci 10-ych do binarnych z okreslona dlugoscia
def dec_2_bin(decimal, length):
    binary = bin(decimal)[2:]
    padded_binary = binary.zfill(length)
    return padded_binary


# sortowanie wartosci wedlug ilosci wystapien w tekscie

# podliczamy ilosc wystapenia kazdego symboli
char_count = Counter(plain_text)

# robimy set (char, freq)
char_frequency_list = [(char, count) for char, count in char_count.items()]

# sortujemy wedlug ilosci wystapien
sorted_char_frequency = sorted(char_frequency_list, key=lambda x: x[1], reverse=True)

# zachowujemy tylko chary
sorted_char_list = [char for char, _ in sorted_char_frequency]

# tworzenie tablicy z wartosciami binarnymi w postaci char
binar = list()
for i in range(u):
    binar.append(dec_2_bin(i, n))

# dodawanie bitow uzupelniajacych do slowniku jezeli sa
if r != 0:
    sorted_char_list.append('eom')
    binar.append(dec_2_bin(u, r))

# tworzenie slowniku zawierajacego {char : bin} (wartosc bin zapisane tez jako char)
char_2_bin_dict = dict(zip(sorted_char_list, binar))

# zapis wartosci binarnych do pliku compressed.txt
with open(compressed_file, "wb") as destination:
    list_of_bools = list()
    # zapisywanie wartosci symboli do tablicy w postaci bool
    try:
        for char in plain_text:
            if char in char_2_bin_dict:
                bin_value = char_2_bin_dict[char]
                for bin_value_to_write in bin_value:
                    if bin_value_to_write == '1':
                        list_of_bools.append(True)
                    else:
                        list_of_bools.append(False)

        # zapisywanie wartosci eom do pliku jezeli sa
        if r != 0:
            for char in char_2_bin_dict['eom']:
                for bin_value_to_write in char:
                    if bin_value_to_write == '1':
                        list_of_bools.append(True)
                    else:
                        list_of_bools.append(False)
    except Exception as e:
        print("Error, probably file is empty", e)

    # tworzymy zmienna dla przechowywania 8 bitow na raz
    chunks = [list_of_bools[i:i + 8] for i in range(0, len(list_of_bools), 8)]

    # zapisujemy bit po bice do pliku
    for chunk in chunks:
        packed_bytes = 0
        for i, bit in enumerate(chunk):
            packed_bytes |= bit << (7 - i)
        destination.write(struct.pack('B', packed_bytes))


# podliczanie koncowego czasu wykonania kompresji
end_time_compression = time.time()
execution_time_compression = end_time_compression - start_time_compression
print("Time it takes to compresss: ", execution_time_compression)


# LOGIKA DLA DEKOMPRESJI PLIKU
# slownik oraz liczba unikalnych wartosci(u) i r pobrane z logiki kompresji
# w razie potrzeby mozna dodac do pliku ktory bedzie zachowywal u oraz klucze slownika kompresji
# oraz ilosc bitow uzupelniajacych na samym poczatku
# (nie jest potrebne do tego skryptu, bo wzsystko zachowane w jednym pliku skryptowym)

# inicjalizowane czasu dla dekompresji
start_time_decompression = time.time()

# pobieranie bajtow z pliku binanrego
with open(compressed_file, "rb") as source:
    packed_data = source.read()

# unpackujemy bajty do postaci bitow(0/1) do tablicy bool_list
bool_list = []
for byte in packed_data:
    for i in range(7, -1, -1):
        bool_list.append((byte >> i) & 1)

# z wartosci int robimy wartosci char dla prawidlowego dzialania slownika
int_2_char_dict = {0: '0', 1: '1'}
bool_list_chars = list()
for value in bool_list:
    bool_list_chars.append(int_2_char_dict[value])

# robimy odwrotny slownik do slownika z kompresja
bin_2_char_dict = {sorted_char_list: binar for binar, sorted_char_list in char_2_bin_dict.items()}

# obcinamy niepotrzbne bity
if r != 0:
    bool_list_chars = bool_list_chars[:-r]

# wycinamy n bitow zapisanych jako char dla prawidlowego uzycia w slowniku
# czyli porownanie odpowiednej liczby bin(zapisanych w postaci char) : char
decompressed_values = list()
for i in range(0, len(bool_list_chars), n):
    bool_list_chars_one_symbol = ''.join(bool_list_chars[i:i+n])
    decompressed_values.append(bin_2_char_dict[bool_list_chars_one_symbol])

# zapis do pliku zdekompresowanego u
with open(uncompressed_file, "w") as f:
    for value in decompressed_values:
        f.write(value)

# podliczanie koncowego czasu wykonania dekompresji
end_time_decompression = time.time()
execution_time_decompression = end_time_decompression - start_time_decompression
print("Time it takes to decompress: ", execution_time_decompression)
