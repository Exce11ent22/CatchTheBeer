from datetime import datetime as dt
from random import randint, uniform


class Game:

    def __init__(self):
        self.p_name = None
        self.field = [0, 0, 0, 0, 0]
        self.start = dt.now()
        self.life = 0
        self.delay = 0
        self.loses = 4
        self.collected = 0
        self.record = self.record_from_file()
        self.collect_time = ''
        self.collect_times = []
        self.best_time = None
        self.saved = False

    def restart(self):
        self.p_name = input("enter ur name: ")
        self.field = [0, 0, 0, 0, 0]
        self.start = dt.now()
        self.life = 0
        self.delay = 5
        self.loses = 0
        self.collected = 0
        self.record = self.record_from_file()
        self.collect_time = 'START'
        self.collect_times = []
        self.best_time = None
        self.saved = False

    def refresh(self):
        if self.time_to_die() and 1 in self.field:
            self.collect_time = 'LOSE'
            i = self.field.index(1)
            self.field[i] = 0
            self.loses += 1
        if self.loses < 3:
            self.spawn()
        if self.loses == 3:
            if not self.saved:
                if len(self.collect_times) == 0:
                    self.best_time = 'No one collected'
                else:
                    self.best_time = str(min(self.collect_times))
                self.change_record()
                self.save_to_log()
                self.saved = True

    def collect(self):
        i = self.field.index(1)
        self.field[i] = 0
        self.collected += 1
        h, m, s = str(dt.now() - self.start).split(":")
        s = str(round(float(s), 3))
        self.collect_times.append(s)
        self.collect_time = s

    def spawn(self):
        if self.time_to_spawn():
            self.field[randint(0, 4)] = 1
            self.start = dt.now()
            self.rand_del()
            self.rand_life()

    def rand_del(self):
        self.delay = uniform(1, 5)

    def rand_life(self):
        self.life = uniform(0.5, 0.9)

    def time_to_die(self):
        result = str(dt.now() - self.start)
        h, m, s = result.split(':')
        s = float(s)
        if s > self.life:
            return True
        return False

    def time_to_spawn(self):
        result = str(dt.now() - self.start)
        h, m, s = result.split(':')
        s = float(s)
        if s > self.delay:
            return True
        return False

    def record_to_file(self):
        with open('record.txt', 'w') as file:
            file.write(str(self.collected))

    def change_record(self):
        if self.collected > self.record:
            self.record_to_file()
            self.record = self.collected

    def save_to_log(self):
        with open('log.txt', 'a') as file:
            file.write(f'player: {self.p_name}; ')
            file.write(f'best_time: {self.best_time}; ')
            file.write(f'player_record: {str(self.collected)}; ')
            file.write(f'session_date: {str(dt.now()).split(".")[0]};\n')

    @classmethod
    def record_from_file(cls):
        with open('record.txt') as file:
            return int(file.read())
