import sys

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication
from janelaPrincipal import JanelaSiViA


if __name__ == '__main__':
    #   rodar
    app = QApplication(sys.argv)
    UIWindow = JanelaSiViA()
    app.exec_()

