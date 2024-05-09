import random
import math
import sympy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256


def generate_rsa_key_pair(key_size=2048, password="private_key", public_key_file="public_key.pem",
                          private_key_file="private_key.pem"):
    """
    Funkcja dla generacji kluczy RSA
    :param private_key_file: file where private key will be stored
    :param public_key_file: file where public key will be stored
    :param password: passphrase to encrypt private key
    :param key_size: dlugosc kluczu
    :return: nic nie zwraca, zapisuje kluczy do plikow .pem
    1)Generujemy pierwsze liczby
    2)Obliczamy e oraz n
    3)Obliczamy d za pomoca biblioteki math
    4)Tworzymy klucz-obiekty za pomoca biblioteki RSA
    5)Szyfrujemy prywatny klucz za pomoca scryptAndAES128-CBC algorytmu
    6)Zapisujemy kluczy do plikow .pem
    """

    # generujemy pierwsze liczbe p i q
    p = sympy.randprime(2 ** (key_size // 2 - 1), 2 ** (key_size // 2))
    q = sympy.randprime(2 ** (key_size // 2 - 1), 2 ** (key_size // 2))
    while q == p:
        q = sympy.randprime(2 ** (key_size // 2 - 1), 2 ** (key_size // 2))

    # obliczamy n
    n = p * q

    # obliczamy phi(n)
    phi_n = (p - 1) * (q - 1)

    # wybieramy liczbe e
    e = random.randrange(3, phi_n)  # Commonly used value
    while True:
        if math.gcd(e, phi_n) == 1:
            break
        e += 1

    # obliczamy d za pomoca wzoru e*d mod phi(n) = 1
    d = sympy.mod_inverse(e, phi_n)

    # tworzymy klucz publiczny za pomoca rsa.construct i zapisujemy go do pliku
    public_key = RSA.construct((n, e))
    public_key_pem = public_key.public_key().export_key('PEM')

    # tworzymy klucz prywatny, szyfrujemy go i zapisujemy do pliku
    private_key = RSA.construct((n, e, d))
    # szyfrowanie klucza za pomoca 'hasla' - scrypt, pozniej szyfrowanie za pomoca algorymtu - AES128-CBC
    # AES - advanced encryption standards, 128 - dlugosc klucza, CBC - cipher block chaining
    private_key_pem = private_key.export_key('PEM', passphrase=password, pkcs=8, protection="scryptAndAES128-CBC")

    with open(public_key_file, "wb") as f:
        f.write(public_key_pem)

    with open(private_key_file, "wb") as f:
        f.write(private_key_pem)


def encrypt_message(message, public_key):
    """
    Funkcja dla szyfrowania informacji
    :param public_key: klucz publiczny dla szyfrowania
    :param message: informacja ktora bedzie zaszyfrowana
    :return: zasyfrowana informacje za pomoca algorytmu RSA, PKCSQ_OAEP padding-algorytm i SHA256 hash-algorytm

    1)Tworzy obiekt dla szyforwania informacji
    2)Szyfrowanie informacji za pomoca wczesniej stworzonego obiektu
    """

    # tworzenie obiektu dla szyfrowania
    hash_object = SHA256.new()
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=hash_object)

    # szyfrowanie za pomoca wczesniej stworzonego obiektu
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message, private_key):
    """
    Funkcja dla deszyfrowania informacji
    :param private_key: prywatny klucz dla deszyfrowania
    :param encrypted_message: zasyfrowana informacja za pomoca klucza publicznego
    :return: zwraca deszyfrowana informacje
    1)Tworzy obiekt dla deszyforwania
    2)Deszyfruje informacje za pomoca wczesniej stworzonego obiektu
    """

    # tworzenie obiektu dla deszyforwania
    hash_object = SHA256.new()
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=hash_object)

    # deszyfrowanie informacji za pomoca wczesniej stworzonego obiektu
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message


def read_public_key(public_key_file="public_key.pem"):
    """
    :param public_key_file: plik do odczytu kluczu publicznego
    Funkcja dla odczytania klucza publicznego
    :return: zwraca odczytany klucz publiczny
    """

    with open(public_key_file, "rb") as f:
        public_key_pem = f.read()
    public_key = RSA.import_key(public_key_pem)
    return public_key


def read_private_key(password=None, private_key_file="private_key.pem"):
    """
    Funkcja dla odczytania klucza prywatnego
    :param private_key_file: plik do odczytu kluczu prywatnego
    :param password: haslo dla deszyfrowania klucza prywatnego
    :return: zwraca odczytany klucz prywatny lub None jezeli passphrase sie nie zgadza
    """

    with open(private_key_file, "rb") as f:
        private_key_pem = f.read()
    try:
        private_key = RSA.import_key(private_key_pem, passphrase=password)
        return private_key
    except ValueError:
        return None
