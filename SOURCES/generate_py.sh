#!/bin/bash

python -m PyQt5.uic.pyuic -x "RNN/Main.ui" -o "../View/RNN/MainWindow.py"
python -m PyQt5.uic.pyuic -x "TSAC/Main.ui" -o "../View/TSAC/MainWindow.py"

python -m PyQt5.uic.pyuic -x "RNN/Database.ui" -o "../View/RNN/DatabaseWindow.py"

python -m PyQt5.uic.pyuic -x "RNN/Administrator.ui" -o "../View/RNN/AdministratorWindow.py"
python -m PyQt5.uic.pyuic -x "TSAC/Administrator.ui" -o "../View/TSAC/AdministratorWindow.py"