"""MainGUI Class"""

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    buttonClickedEventWithArgument = pyqtSignal(str, str)
    simulationInputDataChangedEvent = pyqtSignal(str, int)
    virusInputDataChangedEvent = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self._virus_selection_list = []

        # load ui objects from Qt Designer .ui file
        self._rootWidget = uic.loadUi('.\\gui\\SimulationMainWindow.ui', self)

        # connect slots to the signals from UI elements
        self._rootWidget.sB_simulation_population.valueChanged.connect(
            lambda: self.sB_population_size_valueChanged())

        self._rootWidget.sB_init_infected_population.valueChanged.connect(
            lambda: self.sB_initial_infected_population_valueChanged())

        self._rootWidget.sB_init_population_moving_distance.valueChanged.connect(
            lambda: self.sB_init_population_moving_distance_valueChanged())

        self._rootWidget.pB_init_sim.clicked.connect(lambda: self.pB_init_sim_clicked())

        self._rootWidget.pB_select_virus.clicked.connect(lambda: self.pB_select_virus_clicked())

        self._rootWidget.pB_new_virus.clicked.connect(lambda: self.pB_new_virus_clicked())

        self._rootWidget.pB_update_virus.clicked.connect(lambda: self.pB_update_virus_clicked())

        self._rootWidget.tE_virus_name.textChanged.connect(lambda: self.tE_virus_name_valueChanged())

        self._rootWidget.sB_virus_death_rate.valueChanged.connect(lambda: self.sB_virus_death_rate_valueChanged())

        self._rootWidget.sB_virus_recovery_time.valueChanged.connect(lambda: self.sB_virus_recovery_time_valueChanged())

        self._rootWidget.sB_virus_contagiousness.valueChanged.connect(
            lambda: self.sB_virus_contagiousness_valueChanged())

        self._rootWidget.sB_virus_contagiousness_radius.valueChanged.connect(
            lambda: self.sB_virus_contagiousness_radius_valueChanged())

        self._rootWidget.cB_virus_selection.currentIndexChanged.connect(lambda: self.update_virus_fields())

    def pB_select_virus_clicked(self):
        # get value from comboBox first
        self.buttonClickedEventWithArgument.emit('select_virus', self._rootWidget.cB_virus_selection.currentText())

    def pB_new_virus_clicked(self):
        self.tE_virus_name_valueChanged()
        self.sB_virus_death_rate_valueChanged()
        self.sB_virus_recovery_time_valueChanged()
        self.sB_virus_contagiousness_valueChanged()
        self.sB_virus_contagiousness_radius_valueChanged()

        self.buttonClickedEventWithArgument.emit('add_virus', '')

    def pB_update_virus_clicked(self):
        self.tE_virus_name_valueChanged()
        self.sB_virus_death_rate_valueChanged()
        self.sB_virus_recovery_time_valueChanged()
        self.sB_virus_contagiousness_valueChanged()
        self.sB_virus_contagiousness_radius_valueChanged()

        self.buttonClickedEventWithArgument.emit('update_virus', self._rootWidget.cB_virus_selection.currentText())

    # emitting signals that are connected ot the application controller
    def pB_init_sim_clicked(self):
        self.buttonClickedEventWithArgument.emit('init_sim', self._rootWidget.cB_virus_selection.currentText())
        # population and people settings
        self.sB_population_size_valueChanged()
        self.sB_initial_infected_population_valueChanged()
        self.sB_init_population_moving_distance_valueChanged()

    # virus properties

    def tE_virus_name_valueChanged(self):
        self.virusInputDataChangedEvent.emit('virus_name', self._rootWidget.tE_virus_name.toPlainText())

    def sB_virus_death_rate_valueChanged(self):
        self.virusInputDataChangedEvent.emit('death_rate', str(self._rootWidget.sB_virus_death_rate.value()))

    def sB_virus_recovery_time_valueChanged(self):
        self.virusInputDataChangedEvent.emit('virus_recovery_time',
                                             str(self._rootWidget.sB_virus_recovery_time.value()))

    def sB_virus_contagiousness_valueChanged(self):
        self.virusInputDataChangedEvent.emit('virus_contagiousness',
                                             str(self._rootWidget.sB_virus_contagiousness.value()))

    def sB_virus_contagiousness_radius_valueChanged(self):
        self.virusInputDataChangedEvent.emit('virus_contagiousness_radius',
                                             str(self._rootWidget.sB_virus_contagiousness_radius.value()))

    # simulation properties
    def sB_init_population_moving_distance_valueChanged(self):
        self.simulationInputDataChangedEvent.emit('population_moving_distance_per_day',
                                                  self._rootWidget.sB_init_population_moving_distance.value())

    def sB_population_size_valueChanged(self):
        self.simulationInputDataChangedEvent.emit('population_size',
                                                  self._rootWidget.sB_simulation_population.value())

    def sB_initial_infected_population_valueChanged(self):
        self.simulationInputDataChangedEvent.emit('infected_population_at_start',
                                                  self._rootWidget.sB_init_infected_population.value())

    def update_virus_comboBox(self, virus_list):
        self._virus_selection_list = virus_list
        self._rootWidget.cB_virus_selection.clear()
        for index, virus in enumerate(virus_list):
            self._rootWidget.cB_virus_selection.addItem(virus.get_name())

    def update_virus_fields(self):
        try:
            virus = next(filter(lambda x: x.get_name() == self._rootWidget.cB_virus_selection.currentText(), self._virus_selection_list))
            self._rootWidget.tE_virus_name.setText(virus.get_name())
            self._rootWidget.sB_virus_death_rate.setValue(virus.get_death_rate())
            self._rootWidget.sB_virus_recovery_time.setValue(virus.get_recovery_time())
            self._rootWidget.sB_virus_contagiousness.setValue(virus.get_contagiousness())
            self._rootWidget.sB_virus_contagiousness_radius.setValue(virus.get_contagious_radius())
        except:
            pass