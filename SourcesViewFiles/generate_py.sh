#!/bin/bash
python -m PyQt5.uic.pyuic -x Main.ui -o "../View/MainWindow.py"
python -m PyQt5.uic.pyuic -x Login.ui -o "../View/LoginWindow.py"
python -m PyQt5.uic.pyuic -x Database.ui -o "../View/DatabaseWindow.py"
python -m PyQt5.uic.pyuic -x DataLoad.ui -o "../View/DataLoadWindow.py"
python -m PyQt5.uic.pyuic -x Administrator.ui -o "../View/AdministratorWindow.py"