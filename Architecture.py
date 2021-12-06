import copy
import random
import time

from Agent import *


class Architecture:
    env = []  # environment
    cleaner_pos = []

    def __init__(self):
        self.all_cleaned = False
        self.init_environment()
        self.init_cleaner()

    def init_environment(self):
        file = open('environment.map', 'r').read().splitlines()
        for line in file:
            self.env.append(list(line))

    def init_cleaner(self):
        init = False
        while not init:
            x = random.randint(1, len(self.env) - 2)
            y = random.randint(1, len(self.env[0]) - 2)
            if self.env[x][y] == ' ':
                self.cleaner_pos = [x, y]
                init = True

    def print_map(self):
        for x in range(0, len(self.env)):
            for y in range(0, len(self.env[0])):
                if [x, y] == self.cleaner_pos:
                    print('C', end='')
                else:
                    print(self.env[x][y], end='')
            print()

    def do_action(self, action):
        self.cleaner_pos = copy.deepcopy(action)
        if self.count_dust() == 0:
            self.all_cleaned = True

    def count_dust(self):
        dust_count = 0
        for line in self.env:
            for pixel in line:
                if pixel == 'X':
                    dust_count += 1
        return dust_count

    def run(self):
        self.print_map()
        time.sleep(1)
        while not self.all_cleaned:
            if self.env[self.cleaner_pos[0]][self.cleaner_pos[1]] == 'X':
                print('VACUUMING')
                self.env[self.cleaner_pos[0]][self.cleaner_pos[1]] = ' '
                if self.count_dust() == 0:
                    self.all_cleaned = True
            else:
                action = agent_function(self.env, self.cleaner_pos)
                self.do_action(action)
            self.print_map()
            time.sleep(0.5)


