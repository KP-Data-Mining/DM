#!/bin/bash

python -m PyQt5.uic.pyuic -x "ProgressBar.ui" -o "../VIEWS/ProgressBar.py"

python -m PyQt5.uic.pyuic -x "RNN/Main_Ru.ui" -o "../VIEWS/RNN/MainWindow_Ru.py"
python -m PyQt5.uic.pyuic -x "RNN/Main_Eng.ui" -o "../VIEWS/RNN/MainWindow_Eng.py"
python -m PyQt5.uic.pyuic -x "TSAC/Main_Ru.ui" -o "../VIEWS/TSAC/MainWindow_Ru.py"
python -m PyQt5.uic.pyuic -x "TSAC/Main_Eng.ui" -o "../VIEWS/TSAC/MainWindow_Eng.py"

python -m PyQt5.uic.pyuic -x "RNN/Database_Ru.ui" -o "../VIEWS/RNN/DatabaseWindow_Ru.py"
python -m PyQt5.uic.pyuic -x "RNN/Database_Eng.ui" -o "../VIEWS/RNN/DatabaseWindow_Eng.py"

python -m PyQt5.uic.pyuic -x "RNN/Administrator_Ru.ui" -o "../VIEWS/RNN/AdministratorWindow_Ru.py"
python -m PyQt5.uic.pyuic -x "RNN/Administrator_Eng.ui" -o "../VIEWS/RNN/AdministratorWindow_Eng.py"
python -m PyQt5.uic.pyuic -x "TSAC/Administrator_Ru.ui" -o "../VIEWS/TSAC/AdministratorWindow_Ru.py"
python -m PyQt5.uic.pyuic -x "TSAC/Administrator_Eng.ui" -o "../VIEWS/TSAC/AdministratorWindow_Eng.py"
