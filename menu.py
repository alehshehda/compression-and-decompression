import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox
from compression import compress
from decompression import decompress


# wyswietla pop-up window dla kompresji/dekompresji
def start_compression_decompression_menu():
    app = QApplication(sys.argv)
    window = FileCompressionDialog()
    window.show()
    sys.exit(app.exec_())


# sprawdza czy plik istnieje
def is_valid_file(file_path):
    return os.path.isfile(file_path)


# dopisuje rozszerzenie .txt jezeli uztkownik nie podal
def add_txt_extension(file_name):
    if not file_name.endswith('.txt'):
        return file_name + '.txt'
    return file_name


# class dla pop-up window kompresji/dekompresji
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

        compress_button.clicked.connect(self.on_compress_clicked)
        decompress_button.clicked.connect(self.on_decompress_clicked)

        layout.addWidget(compress_button)
        layout.addWidget(decompress_button)

        self.setLayout(layout)
        self.setWindowTitle("File (de)Compression Tool")

    def on_compress_clicked(self):
        file_path, ok = QInputDialog.getText(self, "Enter File Path", "Enter the path or the name "
                                                                      "of the file to compress:")
        file_path = add_txt_extension(file_path)
        if ok and file_path:
            if not is_valid_file(file_path):
                QMessageBox.critical(self, "Error", "Invalid file path!")
                return
            save_path, ok = QInputDialog.getText(self, "Enter Save Path", "Enter the path or the name "
                                                                          "to save the compressed file:")
            save_path = add_txt_extension(save_path)
            if ok and save_path:
                try:
                    taken_time = compress(file_path, save_path)
                    QMessageBox.information(self, "Success",
                                            f"File successfully compressed!\nTime taken to compress: {taken_time:.2f}"
                                            f" seconds")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Compression failed: {str(e)}")

    def on_decompress_clicked(self):
        file_path, ok = QInputDialog.getText(self, "Enter File Path", "Enter the path or the name "
                                                                      "of the file to decompress:")
        file_path = add_txt_extension(file_path)
        if ok and file_path:
            if not is_valid_file(file_path):
                QMessageBox.critical(self, "Error", "Invalid file path!")
                return

            save_path, ok = QInputDialog.getText(self, "Enter Save Path",
                                                 "Enter the path or the name to save the decompressed file:")
            save_path = add_txt_extension(save_path)
            if ok and save_path:
                try:
                    taken_time = decompress(file_path, save_path)
                    QMessageBox.information(self, "Success",
                                            f"File successfully decompressed!\nTime taken to decompress: "
                                            f"{taken_time:.2f} seconds")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Decompression failed: {str(e)}")
