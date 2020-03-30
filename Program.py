"""Pandemic simulation created by Joshua.
Disclaimer: I'm a self taught software developer with no formal computer science education or any
medical/pandemics/virus background.I do have a Masters degree in mechanical engineering. But that doesn't mean that I
know what im doing ;)

I built this simulator just for the heck of solving the problem while in quarantine at home. If you find any errors,
let me know and I will try to fix them as soon as possible. My goal was to make an easy to use pandemic simulator
available to anyone who was interested in playing around with different parameters that change the behaviour of a
pandemic.

This will NOT predict how the COVID-19 or any pandemic will play out in the real world! There are way too many
variables in the real world that I can't include in the simulation. Have fun with the simulation and stay safe!"""

from PyQt5 import QtWidgets
import sys

from src.controller import ApplicationController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    appCtrl = ApplicationController.AppController()

    sys.exit(app.exec_())
