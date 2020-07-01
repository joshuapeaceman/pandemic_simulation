import math
from copy import deepcopy

import pandas

from src.model import Person
import random
import plotly.graph_objects as go
import plotly.express as px


class Simulation():
    def __init__(self):

        self._person_dictionary = {}
        self._person_list = []

        self._population_size = 1000
        self._initial_infected_population = 1
        self._people_moving_distance_per_day = 25
        self._people_moving_distance_per_day_original = 25

        self._people_moving_distance_per_day_after_reduction = 10
        self._mobility_reduction_start_time = 1000
        self._send_to_hospital_day = 0

        self.day_of_last_known_new_infection = 0
        self._hospital_capacity = 150
        self._hospital_beds_used_cnt = 0
        self._selected_virus = None
        self.stats = []

        self.animation_df = []
        self._simulation_stats_per_day = []

    def run_simulation(self):
        """Creates the initial population set in the GUI. Initializes all simulation parameters."""

        self._simulation_end_flag = False
        self.animation_df.clear()

        self._person_dictionary = {0: [],
                                   1: [],
                                   2: [],
                                   3: [],
                                   4: []}

        # adding sick people to the population
        for i in range(0, self._initial_infected_population):
            person = Person.Person(i, moving_distance=self._people_moving_distance_per_day)
            person.set_health_status_to_infected_at_current_day(0)
            self._person_dictionary[1].append(person)

        # adding healthy people to the population
        for x in range(self._initial_infected_population, self._population_size):
            self._person_dictionary[0].append(Person.Person(x, moving_distance=self._people_moving_distance_per_day))

        print('Initiation done..', self._initial_infected_population, 'people started out sick and ',
              self._population_size - self._initial_infected_population, 'started healthy')

        self.run_simulation_loop()

    def run_simulation_loop(self):
        """Main simulation loop method. This method generates the output for the plot and animation. While the
        simulation_end_flag is set to False the loop will continue incrementing by one for every day of the pandemic.
        Every day all healthy and infected people move by the set distance in a random direction.
        (see Person.update_position()). Then the health status is checked and some people are killed by the virus,
        while others are set to 'Recovered' if they survived for the set duration of the illness
        (see self.update_health_Status()). At last all infected people check their surroundings for health people and
        infect them depending on the contagiousness propability set by the user
        (see self.find_healthy_persons_inside_contagious_radius_and_infect())"""


        self._simulation_end_flag = False
        self.stats.clear()

        day_counter = 0
        self.day_of_last_known_new_infection = 0
        print('starting simulation run..')

        while not self._simulation_end_flag:

            # Update position for all healthy people.
            for idx, aPerson in enumerate(self._person_dictionary[0]):
                aPerson.update_position(self._people_moving_distance_per_day)

            # Update position for all infected people and infect new people. Also check health status changes.
            for idx, aPerson in enumerate(self._person_dictionary[1]):

                aPerson.update_position(self._people_moving_distance_per_day)
                # update health status for infected people (either recovered or killed)
                status = self.update_health_status(aPerson, day_counter, self._person_dictionary,
                                                   idx)

                if status != 'dead' or status != 'recovered':
                    infected = self.find_healthy_persons_inside_contagious_radius_and_infect(aPerson,
                                                                                             day_counter,
                                                                                             self._person_dictionary[
                                                                                                 0])

                    """Set general simulation parameter "day_of_last_known_new_infection" to the current day if someone
                    was infected that day."""
                    if infected == True:
                        self.day_of_last_known_new_infection = day_counter


            """Append current day stats for bar chart"""
            self.stats.append((day_counter,
                               len(self._person_dictionary[0]),
                               len(self._person_dictionary[1]),
                               len(self._person_dictionary[2]),
                               len(self._person_dictionary[3]),
                               len(self._person_dictionary[4]),
                               ))



            active_sick_people = len(self._person_dictionary[1])
            percentage = (active_sick_people / self._population_size) * 100


            """Slow down movement of population if a specific set percentage of the population is infected. If the 
            percentage drops back below the threshold set moving distance back to initial value."""
            if percentage >= (self._mobility_reduction_start_time / 10):
                self._people_moving_distance_per_day = self._people_moving_distance_per_day_after_reduction
            else:
                self._people_moving_distance_per_day = self._people_moving_distance_per_day_original


            """Check to see if we can stop the simulation."""
            if day_counter >= 300 and day_counter > self.day_of_last_known_new_infection + self._selected_virus.get_recovery_time():
                self._simulation_end_flag = True
                print('finished simulation run.. plotting stats... check your browser')
                self.plot_simulation_stats(self.stats)
                ('finished simulation run.. generating animation... check your browser')
                self.generate_animation(self.animation_df)


            """Generate the frames for the scatter plot animation."""
            self.generate_scatter_plot_animation_frames(day_counter, self._person_dictionary)
            day_counter += 1

    def find_healthy_persons_inside_contagious_radius_and_infect(self, current_person, current_day, person_list):
        """This method checks for healthy people inside the contagiouse square of current_person and tries to infect
        them with the virus contagiousness propability """

        infected_flag = False
        # stops person from infecting people on the same day they were infected
        if current_person.get_infection_start_time() < current_day:
            for idx, aPerson in enumerate(person_list):

                # check, if person is inside the contagious radius
                infectious_radius = self._selected_virus.get_contagious_radius()

                dX = aPerson.get_position()[0] - current_person.get_position()[0]
                dY = aPerson.get_position()[1] - current_person.get_position()[1]
                if dX < 0:
                    dX = dX * -1
                if dY < 0:
                    dY = dY * -1

                distance = math.sqrt((dX * dX) + (dY * dY))

                if distance <= infectious_radius:

                    # if a person is still healthy, they can be infected
                    if random.randrange(0, 1000, 1) <= self._selected_virus.get_contagiousness():
                        # aPerson.set_infected_by_virus(current_person.get_infected_by_virus())
                        aPerson.set_health_status_to_infected_at_current_day(current_day=current_day)
                        # remove newly infected person from healthy list and add to the infected list
                        self._person_dictionary[1].append(person_list.pop(idx))

                        infected_flag = True
        return infected_flag

    def update_health_status(self, current_person, current_day, person_dictionary, current_index):
        """This is where the magic happens. This method looks at an infected person, when they were infected and what
        to do with them. We can send people to hospital/quarantine, let them recover or send them to die. Here we can
        add any kind of health state change for an infected person. Feel free to add things..."""


        """Send person to the hospital/quarantine area. They can not infect anyone new there. Also fill as 
        hospital spot with an extra person. This will be undone once the person has recovered or died."""
        if int(current_day - current_person.get_infection_start_time()) == self._send_to_hospital_day:
            if self._hospital_beds_used_cnt < self._hospital_capacity:
                if current_person.get_hospitalized_status() != True:
                    current_person.send_to_hospital()
                    self._hospital_beds_used_cnt += 1

        if current_day - current_person.get_infection_start_time() >= self._selected_virus.get_recovery_time():
            if random.randrange(0, 1000, 1) <= (self._selected_virus.get_death_rate()):
                self._hospital_beds_used_cnt -= 1
                current_person.set_health_status(3)
                current_person.send_to_cemetery()
                person_dictionary[3].append(person_dictionary[1].pop(current_index))
                return 'dead'
            else:
                self._hospital_beds_used_cnt -= 1
                current_person.set_health_status(2)
                current_person.send_to_afterparty()
                person_dictionary[2].append(person_dictionary[1].pop(current_index))
                return 'recovered'

    def generate_scatter_plot_animation_frames(self, day, population):

        for person in population[0]:
            day_plot = {'id': int(person.get_id()),
                        'day': day,
                        'x': int(person.get_position()[0]),
                        'y': int(person.get_position()[1]),
                        'col': "healthy"}
            self.animation_df.append(day_plot)

        for person1 in population[1]:
            day_plot1 = {'id': int(person1.get_id()),
                         'day': day,
                         'x': int(person1.get_position()[0]),
                         'y': int(person1.get_position()[1]),
                         'col': "sick"}
            self.animation_df.append(day_plot1)

        for person2 in population[2]:
            day_plot2 = {'id': int(person2.get_id()),
                         'day': day,
                         'x': int(person2.get_position()[0]),
                         'y': int(person2.get_position()[1]),
                         'col': "recovered"}
            self.animation_df.append(day_plot2)

        for person3 in population[3]:
            day_plot3 = {'id': int(person3.get_id()),
                         'day': day,
                         'x': int(person3.get_position()[0]),
                         'y': int(person3.get_position()[1]),
                         'col': "dead"}
            self.animation_df.append(day_plot3)

        self.animation_df.append({'id': 10000,
                                  'day': day,
                                  'x': 0,
                                  'y': 0,
                                  'col': "recovered"})
        self.animation_df.append({'id': 9999,
                                  'day': day,
                                  'x': 1000,
                                  'y': 1000,
                                  'col': "dead"})

    def plot_simulation_stats(self, stats):
        """This method plots the simulation stats to a plotly stacked bar chart"""
        days = []
        healthy = []
        sick = []
        immune = []
        dead = []
        quarantined = []

        x = 0
        for stat in stats:
            days.append(stat[0])
            healthy.append(stat[1])
            sick.append(stat[2])
            immune.append(stat[3])
            dead.append(stat[4])
            quarantined.append(stat[5])
            x += 1

        fig = go.Figure(data=[
            go.Bar(name='Sick', x=days, y=sick, marker={'color': 'blue'}),
            go.Bar(name='Recovered', x=days, y=immune, marker={'color': 'green'}),
            go.Bar(name='Dead', x=days, y=dead, marker={'color': 'red'}),
            go.Bar(name='Healthy', x=days, y=healthy, marker={'color': 'orange'})])
        # Change the bar mode
        fig.update_layout(barmode='stack',
                          title=self._selected_virus.get_name() + ' raged for ' + str(
                              self.day_of_last_known_new_infection + self._selected_virus.get_recovery_time()) + ' days, infected a total of ' + str(
                              immune[-1] + dead[-1]) + ' and killed ' + str(dead[-1]) + ' people.',
                          xaxis_title="Days of pandemic",
                          yaxis_title="People Count")

        fig.show()

    def generate_animation(self, animation_df):
        df = pandas.DataFrame(animation_df)
        fig2 = px.scatter(data_frame=df, x="x", y="y", animation_frame="day", animation_group="id", color="col",
                          range_x=[-500, 1500], range_y=[-500, 1500])
        fig2.show()

    def set_selected_virus(self, virus):
        self._selected_virus = virus

    def set_initial_infected_population(self, infected_population):
        self._initial_infected_population = infected_population

    def set_send_to_hospital_day(self, day):
        self._send_to_hospital_day = day

    def set_population_size(self, size):
        self._population_size = size

    def set_people_moving_distance_per_day(self, moving_distance):
        self._people_moving_distance_per_day = moving_distance
        self._people_moving_distance_per_day_original = moving_distance

    def set_people_moving_distance_per_day_after_reduction(self, reduced_movement):
        self._people_moving_distance_per_day_after_reduction = reduced_movement

    def set_mobility_reduction_start_time(self, event_time):
        self._mobility_reduction_start_time = event_time

    def set_hospital_capacity(self, no):
        self._hospital_capacity = no
