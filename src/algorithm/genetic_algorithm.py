import random

import numpy as np

from src.data_structure.magic_cube import MagicCube
from src.algorithm.objective_function import ObjectiveFunction

class GeneticAlgorithm:

    def __init__(self, initial_cube : MagicCube, cube_size : int):
        self.POPULATION_COUNT = 300
        self.MAX_ITERATION = 300
        self.MUTATION_CHANCE = 0.2
        self.TARGET_VALUE = 109
        self.cube = initial_cube
        self.cube_size = cube_size
        self.iteration : int = 1
        self.population : list[[MagicCube, int]] = []
        self.range = []
        self.states : list[MagicCube] = []


    def genetic_algorithm(self):
        self.population = self.__create_population()
        for p in self.population:
            if (p[1] == self.TARGET_VALUE):
                self.states.append(p[0])
                return
        best=0
        while(self.iteration <= self.MAX_ITERATION):
            self.__sort_population()
            self.range = self.__create_range()
            children : list[[MagicCube, int]] = []
            for i in range(self.POPULATION_COUNT):
                parent_one, parent_two = self.__get_parents()
                child_one, child_two = self.__reproduce(parent_one, parent_two)
                self.__mutate(child_one)
                self.__mutate(child_two)
                children.append([child_one, ObjectiveFunction.get_object_value(child_one)])
                children.append([child_two, ObjectiveFunction.get_object_value(child_two)])
            for c in children:
                if (c[1] == self.TARGET_VALUE):
                    self.states.append(c[0])
                    return
            best = 0
            best_instance = None
            for c in children:
                if (c[1] > best):
                    best_instance = c[0]
                    best = c[1]
            self.states.append(best_instance)
            self.population = children
            print(best)
            self.iteration += 1
        print(best)
        return


    def get_states(self) -> list[MagicCube]:
        return self.states

    def __create_population(self) -> list[[MagicCube, int]]:
        population_temp = [MagicCube() for _ in range(self.POPULATION_COUNT)]
        ret = []
        for m in population_temp:
            ret.append([m, ObjectiveFunction.get_object_value(m)])
        return ret

    def __sort_population(self):
        return sorted(self.population, key=lambda x: x[1], reverse=True)

    def __create_range(self) -> list[[float, float]]:
        total = 0
        i = 0
        ret = []
        for p in self.population:
            total += p[1]
        for p in self.population:
            ret.append([i, i + (100 * p[1] / total)])
            i += (100 * p[1] / total)
        return ret

    def __get_parents(self) -> tuple[MagicCube, MagicCube]:
        rnd = random.random() * 100
        parent_one, parent_two = None, None
        for i in range(len(self.range)):
            r = self.range[i]
            if r[0] <= rnd <= r[1]:
                parent_one = self.population[i][0]

        rnd = random.random() * 100
        for i in range(len(self.range)):
            r = self.range[i]
            if r[0] <= rnd <= r[1]:
                parent_two = self.population[i][0]

        return parent_one, parent_two

    def __reproduce(self, a : MagicCube, b : MagicCube) -> tuple[MagicCube, MagicCube]:
        crossover_point = random.randint(1, self.cube_size**3-1)
        data_one = np.concatenate((a.data[:crossover_point], b.data[crossover_point:]))
        data_two = np.concatenate((b.data[:crossover_point], a.data[crossover_point:]))
        child_one = MagicCube(self.cube_size, data_one)
        child_two = MagicCube(self.cube_size, data_two)
        return child_one, child_two

    def __mutate(self, m : MagicCube):
        if (random.random() < self.MUTATION_CHANCE):
            i = random.randint(0, self.cube_size**3-1)
            j = random.randint(i, self.cube_size**3-1)
            m.swap_index(i, j)
        return
