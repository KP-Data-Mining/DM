import os

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QWidget
from PyQt5.uic.Compiler.qtproxies import QtGui

external_windows = []
previous_url = []


class MainView(QWebEngineView):
    server = None

    def __init__(self, server, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.server = server

    def closeEvent(self, a0: QtGui.QCloseEvent):
        index = external_windows.index(self)
        external_windows.pop(index)
        previous_url.pop(index)
        self.server.terminate()


class View(QWebEngineView):
    def closeEvent(self, a0: QtGui.QCloseEvent):
        index = external_windows.index(self)
        external_windows.pop(index)
        previous_url.pop(index)


class CustomWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, is_main_frame):
        now_index = len(external_windows)
        if now_index == 0:
            if _type == QWebEnginePage.NavigationTypeRedirect:
                w = View()
                w.setUrl(url)
                w.show()
                external_windows.append(w)
                previous_url.append(url)
                return False
        else:
            if _type == QWebEnginePage.NavigationTypeRedirect and (url not in previous_url):
                w = View()
                w.setUrl(url)
                w.show()
                external_windows.append(w)
                previous_url.append(url)
                return False
            if url in previous_url:
                external_windows[now_index - 1].setFocus(True)
                external_windows[now_index - 1].activateWindow()
        return now_index == 0


class PlotWindow(QWidget):
    def __init__(self, link, server, *args, **kwargs):
        super(PlotWindow, self).__init__(*args, **kwargs)
        vbox = QVBoxLayout(self)
        self.webEngineView = MainView(server)
        self.webEngineView.setPage(CustomWebEnginePage(self))
        self.webEngineView.setUrl(QUrl(link))
        vbox.addWidget(self.webEngineView)
        self.setLayout(vbox)
        self.setWindowTitle('Визуализация')
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if os.path.exists('2.csv'):
            os.remove('2.csv')
        if os.path.exists('3.csv'):
            os.remove('3.csv')
        if os.path.exists('TSAC.html'):
            os.remove('TSAC.html')