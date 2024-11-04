from src.data_structure.magic_cube import MagicCube
from src.algorithm.objective_function import ObjectiveFunction

import random
import math


class SimulatedAnnealing:
    """
    Implementation of simulated annealing algorithm

    :var INITIAL_TEMPERATURE: constant of initial temperature of algorithm
    :var cube: The initial of a magic cube
    :var objective: The objective value of current state
    :var time: The time variable for iteration
    """

    def __init__(self, initial_cube, cube_size):
        """
        Initialization for the algorithm

        :param initial_cube: The initial magic cube object before algorithm starts
        :param cube_size: The size of initial magic cube
        """

        # CONSTANTS (Algorithm Settings)
        self.INITIAL_TEMPERATURE = 2
        self.MAX_TIME = 250000
        # self.MAX_TIME = 1000
        self.TARGET_VALUE = 109
        self.time = 1
        self.cube = initial_cube
        self.objective = ObjectiveFunction.get_object_value(initial_cube)
        self.size = cube_size
        self.states: list[MagicCube] = [initial_cube]
        self.data_per_iteration: list[float] = []
        self.stuck_frequency: int = 0

    def simulated_annealing(self):
        """
        Execute the Algorithm
        """
        if not self.cube.is_perfect():
            while self.time <= self.MAX_TIME:
                neighbor, neighbor_objective = self.__get_random_neighbor()
                if neighbor_objective == self.TARGET_VALUE:
                    self.states.append(neighbor)
                    break
                if neighbor_objective > self.objective:
                    self.states.append(neighbor)
                    self.cube = neighbor
                    self.objective = neighbor_objective

                    print("State " + str(self.time) + " with value " + str(neighbor_objective) + " and current " +
                        str(self.objective) + " is better")

                else:
                    delta_E = neighbor_objective - self.objective
                    if self.__accept_by_probability(delta_E, self.time):
                        if delta_E < 0:
                            self.states.append(neighbor)
                            self.stuck_frequency += 1
                        self.cube = neighbor
                        self.objective = neighbor_objective
                        temperature: float = self.INITIAL_TEMPERATURE / math.log(self.time + 1)
                        probability: float = math.exp(delta_E / temperature)
                        self.data_per_iteration.append(probability)
                        # if delta_E < 0:
                        #     print("State " + str(self.time) + " with value " + str(neighbor_objective) + " and current "
                        #           + str(self.objective) + " with probability " + str(probability) + " E = " +
                        #           str(delta_E))
                self.time += 1
        return

    def get_states(self) -> list[MagicCube]:
        return self.states

    def get_probability_per_iteration(self) -> list[float]:
        return self.data_per_iteration

    def get_stuck_frequency(self) -> int:
        return self.stuck_frequency

    # -- INTERNAL FUNCTION --

    def __get_random_neighbor(self) -> [MagicCube, int]:
        """
        Returns a random neighbor and it's value
        """
        i = random.randint(0, self.size ** 3 - 1)
        j = random.randint(i, self.size ** 3 - 1)
        neighbor: MagicCube = self.cube.swap_index_copy(i, j)
        neighbor_objective: int = ObjectiveFunction.get_object_value(neighbor)
        return [neighbor, neighbor_objective]

    def __accept_by_probability(self, delta_e, time) -> bool:
        temperature: float = self.INITIAL_TEMPERATURE / math.log(time + 1)
        probability: float = math.exp(delta_e / temperature)
        return random.random() < probability
