from src.model import Person
import random
import plotly.graph_objects as go


class Simulation:
    def __init__(self):

        self._person_dictionary = {}
        self._person_list = []

        self._population_size = 1000
        self._initial_infected_population = 1
        self._people_moving_distance_per_day = 10

        self._selected_virus = None

        self._day_counter = 0

        # end simulation while loop flag
        self._simulation_end_flag = False

        self._simulation_stats_per_day = []

    def start_simulation(self):
        self.run_simulation_loop()

    def initiate_simulation(self):
        self._simulation_end_flag = False

        self._person_dictionary = {0: [],
                                   1: [],
                                   2: [],
                                   3: [],
                                   4: []}

        # adding sick people to the population
        for i in range(0, self._initial_infected_population):
            person = Person.Person(moving_distance=self._people_moving_distance_per_day)
            person.set_health_status_to_infected(0)
            person.set_infected_by_virus(self._selected_virus)
            self._person_dictionary[1].append(person)

        # adding healthy people to the population
        for x in range(self._initial_infected_population, self._population_size):
            self._person_dictionary[0].append(Person.Person(moving_distance=self._people_moving_distance_per_day))

        print('Initiation done..', self._initial_infected_population, 'people started out sick and ',
              self._population_size - self._initial_infected_population, 'started healthy')
        self.run_simulation_loop()

    def run_simulation_loop(self):
        stats = []
        self._day_counter = 0
        last_know_new_infection = 0
        print('starting simulation run..')

        while not self._simulation_end_flag:

            self._person_dictionary[0].sort(key=lambda x: x.get_position()[0])
            self._person_dictionary[0].sort(key=lambda x: x.get_position()[1])

            for idx, aPerson in enumerate(self._person_dictionary[0]):
                aPerson.update_position()

            for idx, aPerson in enumerate(self._person_dictionary[1]):
                # check if person survived or kill them

                aPerson.update_health_status(self._day_counter, self._person_dictionary, idx)
                aPerson.update_position()
                infected = self.find_healthy_persons_inside_contagious_radius_and_infect(aPerson,
                                                                                         self._day_counter,
                                                                                         self._person_dictionary[
                                                                                             0])
                if infected[0] == True:
                    last_know_new_infection = self._day_counter

            stats.append((self._day_counter,
                          len(self._person_dictionary[0]),
                          len(self._person_dictionary[1]),
                          len(self._person_dictionary[2]),
                          len(self._person_dictionary[3]),
                          len(self._person_dictionary[4])))
            print('day: ', self._day_counter)

            # when there are no more infected people who could spread the virus stop simulation
            if self._day_counter > last_know_new_infection + self._selected_virus.get_recovery_time() and len(
                    self._person_dictionary[1]) == 0:
                self._simulation_end_flag = True
                print('finished simulation run.. plotting in...')
                self.plot_simulation_stats(stats)

            self._day_counter += 1

    def find_healthy_persons_inside_contagious_radius_and_infect(self, current_person, current_day, person_list):
        infected_flag = False
        infected_cnt = 0
        # stop me from infecting people on the same day i got infected
        if current_person.get_infection_start_time() < current_day:
            for idx, aPerson in enumerate(person_list):
                # inside contagious radius
                if (aPerson.get_position()[0] >= (current_person.get_position()[0] -
                                                  current_person.get_infected_by_virus().get_contagious_radius())) and (
                        aPerson.get_position()[0] <= (current_person.get_position()[0] +
                                                      current_person.get_infected_by_virus().get_contagious_radius())) and (
                        aPerson.get_position()[1] >= (current_person.get_position()[1] -
                                                      current_person.get_infected_by_virus().get_contagious_radius())) and (
                        aPerson.get_position()[1] <= (current_person.get_position()[1] +
                                                      current_person.get_infected_by_virus().get_contagious_radius())):
                    # if a person is still healthy, they can be infected
                    if random.randrange(0, 1000, 1) <= current_person.get_infected_by_virus().get_contagiousness():
                        aPerson.set_infected_by_virus(current_person.get_infected_by_virus())
                        aPerson.set_health_status_to_infected(current_day=current_day)
                        self._person_dictionary[1].append(person_list.pop(idx))
                        infected_cnt += 1
                        infected_flag = True
        return (infected_flag, infected_cnt)

    def plot_simulation_stats(self, stats):

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
            go.Bar(name='Sick', x=days, y=sick),
            go.Bar(name='Immune', x=days, y=immune),
            go.Bar(name='Dead', x=days, y=dead),
            go.Bar(name='Quarantine', x=days, y=quarantined),
            go.Bar(name='Healthy', x=days, y=healthy)])
        # Change the bar mode
        fig.update_layout(barmode='stack',
                          title=self._selected_virus.get_name() + ' raged for ' + str(
                              self._day_counter) + ' days, infected a total of ' + str(immune[-1]+dead[-1]) +' and killed ' + str(dead[-1]) + ' people.',
                          xaxis_title="Days of pandemic",
                          yaxis_title="People Count" )

        fig.show()

    def get_person_list(self):
        return self._person_list

    def set_selected_virus(self, virus):
        self._selected_virus = virus

    def set_initial_infected_population(self, infected_population):
        self._initial_infected_population = infected_population

    def set_population_size(self, size):
        self._population_size = size

    def set_people_moving_distance_per_day(self, moving_distance):
        self._people_moving_distance_per_day = moving_distance
