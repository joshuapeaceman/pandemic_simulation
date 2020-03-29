import random
import math


class Person:
    def __init__(self,  moving_distance):
        self._position = (random.randrange(25, 975, 1), random.randrange(25, 975, 1))
        self._moving_distance = moving_distance
        self._moving_direction = random.randrange(0, 360, 1)
        self._infected_by_virus = None
        self._health_status = 0
        self._infection_start_time = 0

    # print('Person ID:', self._id, 'x_pos:', self._position[0], 'y_pos:', self._position[1], 'health_status:', self._health_status)

    def update_position(self):
        radians = math.radians(random.randrange(0, 360, 1))

        new_x_pos = self._position[0] + int(math.cos(radians) * self._moving_distance)
        new_y_pos = self._position[1] + int(math.sin(radians) * self._moving_distance)
        if new_x_pos >= 0 and new_x_pos <= 1000 and new_y_pos >= 0 and new_y_pos <= 1000:
            self._position = (new_x_pos, new_y_pos)
        else:
            self.update_position()


    def set_health_status_to_infected(self, current_day):
        self._health_status = 1
        self._infection_start_time = current_day

    def update_health_status(self, current_day, person_dictionary, current_index):
        if self._infection_start_time < current_day:
            if random.randrange(0, 1000, 1) <= self._infected_by_virus.get_death_rate():
                self._health_status = 3
                person_dictionary[3].append(person_dictionary[1].pop(current_index))
            elif self._infection_start_time == current_day - 1:
                # self._health_status = 4
                # person_dictionary[4].append(person_dictionary[1].pop(current_index))
                pass
            else:
                if current_day - self._infection_start_time >= self._infected_by_virus.get_recovery_time():
                    self._health_status = 2
                    person_dictionary[2].append(person_dictionary[1].pop(current_index))

    def set_infected_by_virus(self, virus):
        self._infected_by_virus = virus

    def get_id(self):
        return self._id

    def get_position(self):
        return self._position

    def get_moving_speed(self):
        return self._moving_distance

    def get_moving_direction(self):
        return self._moving_direction

    def get_infected_by_virus(self):
        return self._infected_by_virus

    def get_health_status(self):
        return self._health_status

    def get_infection_start_time(self):
        return self._infection_start_time

    def set_infection_start_time(self, start_time):
        self._infection_start_time = start_time
