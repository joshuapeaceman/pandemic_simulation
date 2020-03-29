"""Pandemic simulation """

from PyQt5 import QtWidgets
import sys

from src.controller import ApplicationController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    appCtrl = ApplicationController.AppController()

    sys.exit(app.exec_())
