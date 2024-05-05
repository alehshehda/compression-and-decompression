Script written in python 3.10, make sure you have installed it or newer version, used libraries: os, sys, math, collections, time, struct, 
random, sympy, Crypto(pycryptodome), PyQt5.QtWidgets


Script implements logic of data compression and decompression **FOR THE .TXT FILES** with the usage of RSA encryption and decryption.
Compression based on simplified Huffman and binary coding, encryption method uses Public Key to encrypt data and decryption
is achieved with the Private Key.
Public and Private Keys can be generated with the function listed in GUI 'Generate RSA key pair' and stored in the same
directory in .pem format. Public Key written as it is, however Private Key has additional layer of security, it is 
encrypted using scryptAndAES128-CBC method. In order to decrypt and use Private Key user must enter password(passphrase) with which
Private Key has been encrypted.

In order to run this code you need to install packages that are listed in 'requirements.txt' using  
`pip install -r requirements.txt` or install them manually.
It is better to install them in the virtual environment, not globally.  
In order to create venv:  
1)Open terminal(for Unix/macOS) or PowerShell(for Windows)  
2)Navigate to the directory, where you downloaded project files, using `cd Path/to/folder`  
3)Type `python -m venv venv` or `python3 -m venv venv` -  second argument is the name of virtual environment that you are creating, you can choose different name  
(you may be asked to install other packages to create venv, it depends on OS that you are using, download them)  
4)Activate your venv, depending on your OS:  
Windows:  
`.\venv\Scripts\activate`  

Unix/MacOS:  
`source venv/bin/activate`    

in this step, 'venv' is the name of virtual environment, so type here the name you used as a second argument in `python -m venv venv` while creating venv  
5)Type `pip install -r requirements.txt` to install needed packages  
After that you can successfully run the script by typing `./main.py` for Unix/macOS or `python main.py` for Windows  
Don't forget to give permission to run this program, `chmod +x main.py` for Unix/macOS or run as administrator if you are using Windows  
<br>
<br>
In order to delete venv:  
1)Open terminal(for Unix/macOS) or PowerShell(for Windows)  
2)Navigate to the directory with the virtual environment you want to delete, using `cd Path/to/folder`  
2)Type `deactivate` in order to deactivate your venv  
3)Delete your venv, depending on your OS:  
Windows:  
`Remove-Item -Path .\venv -Recurse -Force`  

Unix/MacOS:  
`rm -rf venv`  

in this step, 'venv' is the name of virtual environment, so type here the name you used as a second argument in `python -m venv venv` while creating venv4
