


class Virus:
    name: str
    recovery_time: int
    death_rate: int
    contagiousness: int
    contagious_radius: int

    def __init__(self, name, recovery_time, death_rate, contagiousness, contagious_radius):
        self._name = name
        self._recovery_time = recovery_time
        self._death_rate = death_rate
        self._contagiousness = contagiousness
        self._contagious_radius = contagious_radius


    def set_name(self, name):
        self._name = name

    def set_recovery_time(self, recovery_time):
        self._recovery_time = recovery_time

    def set_death_rate(self, death_rate):
        self._death_rate = death_rate

    def set_contagiousness(self, contagiousness):
        self._contagiousness = contagiousness

    def set_contagious_radius(self, contagious_radius):
        self._contagious_radius = contagious_radius

    def get_name(self):
        return self._name

    def get_recovery_time(self):
        return self._recovery_time

    def get_death_rate(self):
        return self._death_rate

    def get_contagiousness(self):
        return self._contagiousness

    def get_contagious_radius(self):
        return self._contagious_radius

