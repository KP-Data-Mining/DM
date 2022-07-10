#!/bin/bash

python -m PyQt5.uic.pyuic -x RNN/Main.ui -o "../VIEWS/RNN/MainWindow.py"
python -m PyQt5.uic.pyuic -x TSAC/Main.ui -o "../VIEWS/TSAC/MainWindow.py"

python -m PyQt5.uic.pyuic -x RNN/Database.ui -o "../VIEWS/RNN/DatabaseWindow.py"

python -m PyQt5.uic.pyuic -x RNN/Administrator.ui -o "../VIEWS/RNN/AdministratorWindow.py"
python -m PyQt5.uic.pyuic -x TSAC/Administrator.ui -o "../VIEWS/TSAC/AdministratorWindow.py"
