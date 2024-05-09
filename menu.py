import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox,
                             QLineEdit, QFileDialog)
from compression import compress
from decompression import decompress
from encryption import generate_rsa_key_pair, read_private_key, read_public_key


def start_compression_decompression_menu():
    """
    Funkcja ktora wyswietla GUI
    """
    app = QApplication(sys.argv)
    window = FileCompressionDialog()
    window.show()
    sys.exit(app.exec_())


def is_valid_file(file_path):
    """
    Funkcja sprawdza czy plik istnieje i czy sa prawa na czytanie tego pliku
    :param file_path: plik ktory bedzie sprawdzony
    :return: True/False
    """
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def add_txt_extension(file_name):
    """
    Funkcja dodaje rozszerzenie .txt do pliku jezeli nie podane
    :param file_name: plik do ktorego bedzie dodano rozszerzenie jezeli go nie ma
    :return: plik z rozszerzeniem .txt
    """
    if not file_name.endswith('.txt'):
        return file_name + '.txt'
    return file_name


class FileCompressionDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("What do you want to do?")
        layout.addWidget(label)

        compress_button = QPushButton("Compress File")
        decompress_button = QPushButton("Decompress File")
        generate_keys_button = QPushButton("Generate RSA Key Pair")

        compress_button.clicked.connect(self.on_compress_clicked)
        decompress_button.clicked.connect(self.on_decompress_clicked)
        generate_keys_button.clicked.connect(self.on_generate_keys_clicked)

        layout.addWidget(compress_button)
        layout.addWidget(decompress_button)
        layout.addWidget(generate_keys_button)

        self.setLayout(layout)
        self.setWindowTitle("File (de)Compression Tool")

    def on_compress_clicked(self):
        file_path = self.get_file_path("Select file to compress")
        if file_path:
            save_path = self.process_file(file_path, compress, "compression")

            save_path_size = os.path.getsize(save_path)
            file_path_size = os.path.getsize(file_path)
            # jezeli kompresja udana
            if save_path_size < file_path_size:
                size_of_compressed_data_bytes = file_path_size - save_path_size

                # liczenie danych ile miejsca skopmresowalo sie
                size_of_compressed_data_mb = size_of_compressed_data_bytes / (1024 * 1024)  # 1 MB = 1024 * 1024 bitow
                size_of_compressed_data_percentage = ((file_path_size - save_path_size) / file_path_size) * 100

                # wyswietlanie tych danych
                QMessageBox.information(self, "Success", f"Size of compressed data: {size_of_compressed_data_mb:.2f} MB"
                                                         f" or {size_of_compressed_data_percentage:.2f}% f"
                                                         f"rom original size")
            # jezeli kompresja nieduana:(
            if save_path_size > file_path_size:
                reply = QMessageBox.question(self, "Warning", "Compressed file takes more space then original file,"
                                                              " do you want to save compressed file?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    os.remove(save_path)

    def on_decompress_clicked(self):
        file_path = self.get_file_path("Select file to decompress")
        if file_path:
            self.process_file(file_path, decompress, "decompression", True)

    def get_file_path(self, dialog_title):
        """
        Funkcja pobiera sciezke lub imie do pliku zrodlowego
        :param dialog_title: Co bedzie wyswetlono jako naglowek
        :return: zwraca sciezke pliku zrodlowego
        """
        file_path, _ = QFileDialog.getOpenFileName(self, dialog_title, "", "Text Files (*.txt)")
        return file_path

    def process_file(self, file_path, operation, operation_name, is_decompression=False):
        """
        Funkcja zajmuje sie obsluga pliku w zaleznosci od podanych argumentow
        :param file_path: plik zrodlowy
        :param operation: ktora funkcja bedze wykorzystywana dla oblsugi pliku: compress or decompress
        :param operation_name: imie funkcji dla interakcji z uzytkownikiem
        :param is_decompression: bool argument zajmuje sie dekompresja pliku jezeli True
        :return: nic nie zwraca, zapisuje obsluzony plik
        """
        # sprawdzanie pliku zrodlowego, czy on instnieje i czy sa prawa dla odczytu tego pliku
        if not is_valid_file(file_path):
            QMessageBox.critical(self, "Error", "Invalid file path or no permission to read the file!")
            return
        # pobieranie pliku docelowego i dodawanie .txt jezeli uzytkownik nie podal
        save_path, ok = QInputDialog.getText(self, "Enter Save Path", f"Enter path or name to save the {operation_name}"
                                                                      f" file:")
        save_path = add_txt_extension(save_path)

        # jezeli taki plik juz istnieje pytamy u uzytkownika czy nadpisac plik
        while ok and save_path and os.path.isfile(save_path):
            reply = QMessageBox.question(self, 'File Exists', 'A file with the same name already exists. Do you want to'
                                                              ' overwrite it?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                break
            save_path, ok = QInputDialog.getText(self, "Enter Save Path", "Enter a different path or name to save the"
                                                                          " compressed file:")
            save_path = add_txt_extension(save_path)

        # jezeli wszystko ok to przechodzimy do kompresji, lub dekompresji jezeli podano True jako ostatni argument
        if ok and save_path:
            try:
                if is_decompression:
                    password, ok = QInputDialog.getText(self, "Enter Password", "Enter password to decrypt private key:"
                                                        , QLineEdit.Password)
                    key = read_private_key(password, private_key_file="private_key.pem")
                    if key is None:
                        QMessageBox.critical(self, "Error", "Incorrect password!")
                        return
                else:
                    key = read_public_key()
                taken_time = operation(file_path, save_path, key)
                QMessageBox.information(self, "Success", f"File {operation_name} has been successful!\nTime "
                                                         f"taken to {operation_name}: {taken_time:.2f} seconds")
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "File not found!")
            except PermissionError:
                QMessageBox.critical(self, "Error", "No permission to read the file!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{operation_name.capitalize()} failed: {str(e)}")

        if not is_decompression:
            return save_path

    def on_generate_keys_clicked(self):

        reply = QMessageBox.question(self, 'Warning', "If you proceed this operation, existing Public and Private Keys "
                                                      "will be replaced with new ones, messages encrypted with existing"
                                                      "Public Key will not be possible to decrypt with paired "
                                                      "Private Key, do you want to proceed?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                password, ok = QInputDialog.getText(self, "Enter Password", "Enter password to encrypt private key:"
                                                    , QLineEdit.Password)
                if password is None:
                    password, ok = QInputDialog.getText(self, "Enter Password", "Password can't be empty:"
                                                        , QLineEdit.Password)
                generate_rsa_key_pair(2048, password, public_key_file="public_key.pem",
                                      private_key_file="private_key.pem")
                QMessageBox.information(self, "Success", "RSA key pair generated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Key generation failed: {str(e)}")
        else:
            QMessageBox.information(self, "Information", "Old keys have been kept")
