import struct
import time
import math
from encryption import decrypt_message
from compression import dec_to_bin


def decompress(to_decompress_file, decompressed_file, private_key):
    """
    FUNKCJA DLA DEKOMPRESJI PLIKU
    :param to_decompress_file: skompresowany plik zawartosc ktorego trzeba zdekompresowac
    :param decompressed_file: plik zdekompresowany
    :param private_key: klucz prywatny RSA za pomoca ktorego bedzie robiona deszyfracja

    1)Pobieranie z pliku zrodlowego potrzebnych wartosci:
    bity uzupelniajace, ilosc bajtow ktore zajete przez szyfrowane unikalne wartosci, szyfrowane unikalne wartosci
    2)Deszyfrowanie unikalnych wartosci za pomoca kluczu prywatnego i algorytmu RSA
    3)Obliczanie potrzebnych zmiennych: ilosc unikalnych wartosci, ilosc bitow potrzebnych do zapisania jednej wartosci
    4)Tworzenie tablicy dla zachowania wartosc base2 zachowanych w postaci char
    5)Tworzenie slownika {bin : char}, wartosci bin zapisane jako char(przy pomocy kroku 4)
    6)Z kazdego bajta wyciagamy bity i wrzucamy do zmiennej dla zachowania wartosci jedno-bitowych
    7)W zmiennej z kroku 5 dla zachowania wartosci jedno-bitowych, dane int przeksztalcamy do typu char
    8)Obcinamy bity uzupelnijace
    7)Dla zmiennej z kroku 6-7 bierzemy n('ilosc bitow potrzebnych do zapisania jednej wartosci' z kroku 3) bitow dla
    prawidlowej dekompresji i zapisujemy do odpowiednej zmiennej
    8)Zapis danych do pliku docelowego
    9)Zwracanie calkowitego czasu wykonania dekompresji
    """

    # inicjalizowane czasu dla dekompresji
    start_time_decompression = time.time()

    # pobieramy liczby uniklanych wartosci, unikalnych wartosci oraz bitow uzupelniajacych
    with open(to_decompress_file, 'rb') as source:
        padding_bits = ord(source.read(1))  # bity uzupelniajace
        sorted_char_list_encrypted_length = struct.unpack('I', source.read(4))[0]  # ilosc bitow zajetych
        # przez zasyfrowane dane
        sorted_char_list_encrypted = source.read(sorted_char_list_encrypted_length)  # zasyfrowane dane
        packed_data = source.read()  # dane dla dekompresji

    # deszyfrowanie unikalnyc wartosci za pomoca kluczu prywatnego
    sorted_char_list_decrypted = decrypt_message(sorted_char_list_encrypted, private_key)
    unique_chars = len(sorted_char_list_decrypted)  # liczba unikalnych wartosci
    bits_per_char = math.ceil(math.log(unique_chars, 2))  # ilosc bitow ktore potrzebne dla zapisu jednej wartosci

    # tworzenie tablicy dla wartosci base2(zapisanych jako char)
    binary_list = list()
    for i in range(unique_chars):
        binary_list.append(dec_to_bin(i, bits_per_char))

    # tworzenie slownika {bin : char} (wartosci bin zapisane tez jako char)
    bin_to_char_dict = dict(zip(binary_list, sorted_char_list_decrypted))

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
        binary_to_decompress = ''.join(char_bool_list[i:i + bits_per_char])
        decompressed_data.append(bin_to_char_dict[binary_to_decompress])

    # zapis do pliku zdekompresowanego
    with open(decompressed_file, "w") as f:
        for value in decompressed_data:
            f.write(value)

    # podliczanie koncowego czasu wykonania dekompresji
    end_time_decompression = time.time()
    execution_time_decompression = end_time_decompression - start_time_decompression
    return execution_time_decompression
