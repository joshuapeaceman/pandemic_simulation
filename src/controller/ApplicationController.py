import os
import sys
from pathlib import Path

from src.gui import MainWindow
from src.simulation import Simulation
from src.model import TheVirus
import json


class AppController:
    def __init__(self):

        self._virus_list = []
        self._virus_name = ''
        self._virus_death_rate = 0
        self._virus_recovery_time = 0
        self._virus_contagiousness = 0
        self._virus_contagiousness_radius = 0

        self._mainWindow = None
        self._initiate_mainWindow()

        self._simulation = Simulation.Simulation()
        self.load_virus_from_file()

    def _initiate_mainWindow(self):
        self._mainWindow = MainWindow.MainWindow()
        # connect the signals sent from MainWindow to slots inside the AppController class
        self._mainWindow.simulationInputDataChangedEvent.connect(self.input_data_changed_interaction_factory_method)
        self._mainWindow.buttonClickedEventWithArgument.connect(self.button_interaction_factory_method)
        self._mainWindow.virusInputDataChangedEvent.connect(self.virus_data_changed_interaction_factory_method)
        self._mainWindow.show()

    def button_interaction_factory_method(self, clicked_button, value):
        # print(clicked_button, 'was clicked')
        button_action_switcher = {
            'init_sim': self.initiate_simulation,
            'add_virus': self.add_virus,
            'select_virus': self.select_virus,
            'update_virus': self.update_virus
        }

        button_action_switcher.get(clicked_button, lambda: 'Invalid')(value)

    def input_data_changed_interaction_factory_method(self, textEdit, value):
        # print(textEdit, value)
        input_data_changed_switcher = {
            'population_size': self.set_simulation_population_size,
            'infected_population_at_start': self.set_infected_population_at_start,
            'population_moving_distance_per_day': self.set_population_moving_distance_per_day

        }
        input_data_changed_switcher.get(textEdit)(value)

    def virus_data_changed_interaction_factory_method(self, inputBox, value):
        input_data_changed_switcher = {
            'virus_name': self.set_virus_name,
            'death_rate': self.set_virus_death_rate,
            'virus_recovery_time': self.set_virus_recovery_time,
            'virus_contagiousness': self.set_virus_contagiousness,
            'virus_contagiousness_radius': self.set_contagiousness_radius
        }
        input_data_changed_switcher.get(inputBox)(value)

    def set_population_moving_distance_per_day(self, distance):
        self._simulation.set_people_moving_distance_per_day(distance)

    def set_simulation_population_size(self, size):
        self._simulation.set_population_size(size)

    def set_infected_population_at_start(self, var):
        self._simulation.set_initial_infected_population(var)

    def add_virus(self, var):
        aVirus = TheVirus.Virus(name=self._virus_name,
                                recovery_time=self._virus_recovery_time,
                                death_rate=self._virus_death_rate,
                                contagiousness=self._virus_contagiousness,
                                contagious_radius=self._virus_contagiousness_radius)

        self._virus_list.append(aVirus)
        self.write_viurses_to_file(self._virus_list)
        self._mainWindow.update_virus_comboBox(self._virus_list)

    def select_virus(self, var):
        aVirus = next(filter(lambda x: x.get_name() == var, self._virus_list))
        self._simulation.set_selected_virus(aVirus)

    def update_virus(self, var):
        index = 0
        for idx, virus in enumerate(self._virus_list):
            if virus.get_name() == var:
                index = idx
        self._virus_list[index].set_name(self._virus_name)
        self._virus_list[index].set_death_rate(self._virus_death_rate)
        self._virus_list[index].set_contagiousness(self._virus_contagiousness)
        self._virus_list[index].set_contagious_radius(self._virus_contagiousness_radius)

        self.write_viurses_to_file(self._virus_list)
        self._mainWindow.update_virus_comboBox(self._virus_list)


    def set_virus_name(self, virus_name):
        self._virus_name = virus_name

    def set_virus_death_rate(self, death_rate):
        self._virus_death_rate = int(death_rate)

    def set_virus_recovery_time(self, recovery_time):
        self._virus_recovery_time = int(recovery_time)

    def set_virus_contagiousness(self, contagiousness):
        self._virus_contagiousness = int(contagiousness)

    def set_contagiousness_radius(self, contagious_radius):
        self._virus_contagiousness_radius = int(contagious_radius)

    def initiate_simulation(self, var):
        self._simulation.set_selected_virus(next(filter(lambda x: x.get_name() == var, self._virus_list)))
        self._simulation.initiate_simulation()

    def get_mainWindow(self):
        return self._mainWindow

    def get_simulation(self):
        return self._simulation

    def load_virus_from_file(self):
        try:
            self._virus_list.clear()
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            elif __file__:
                application_path = Path(__file__).parent.parent.parent

            dir_path = str(application_path)
            with open(dir_path + '\\ressources\\virus_lib.json') as json_file:
                data = json.load(json_file)
                for v in data['viruses']:
                    self._virus_list.append(TheVirus.Virus(v['name'],
                                                           v['recovery_time'],
                                                           v['death_rate'],
                                                           v['contagiousness'],
                                                           v['contagious_radius']))
            self._mainWindow.update_virus_comboBox(self._virus_list)

        except:
            pass

    def write_viurses_to_file(self, viurs_list):
        data = {}
        data['viruses'] = []

        for aVirus in viurs_list:
            data['viruses'].append({'name': aVirus.get_name(),
                                    'recovery_time': aVirus.get_recovery_time(),
                                    'death_rate': aVirus.get_death_rate(),
                                    'contagiousness': aVirus.get_contagiousness(),
                                    'contagious_radius': aVirus.get_contagious_radius()
                                    })

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = Path(__file__).parent.parent.parent

        dir_path = str(application_path)
        with open(dir_path + '\\ressources\\virus_lib.json', 'w') as outfile:
            json.dump(data, outfile)
