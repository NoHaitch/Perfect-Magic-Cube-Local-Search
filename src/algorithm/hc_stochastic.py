from data_structure.magic_cube import MagicCube

import random


class StochasticHillClimb:
    """
    A local search algorithm: Stochastic Hill-Climbing without temperature control.
    """
    def __init__(self, initial_cube: MagicCube):
        self.states: list[MagicCube] = [initial_cube]   # self.states[-1] is the current state
        self.iteration_value: list[int] = []

    def stochastic_hill_climb(self, nmax: int) -> tuple[list[any], int, list[int]]:
        """
        Executes the Stochastic Hill Climbing algorithm for a maximum of nmax iterations.
        Returns the best state and the number of iterations performed.
        """
        current = self.states[-1].copy()            # Copy of the initial cube
        current_value = current.get_state_value()   # Initial state value
        self.iteration_value.append(current_value)
        i = 0                                        # Initiation of the number of iterations

        # Loop of stochastic hill-climbing
        while i < nmax:
            # Generate neighbors
            neighbors = self.__generate_neighbors()
            if not neighbors or current_value == 109:
                break

            # Randomly select a neighbor
            neighbor = random.choice(neighbors)
            neighbor_value = neighbor.get_state_value()
            self.iteration_value.append(neighbor_value)

            # Always accept the neighbor if it's better
            if neighbor_value > current_value:
                self.states.append(neighbor)
                current_value = neighbor_value

            i += 1
            print("iteration", i, "- current value", current_value)

        return self.states, i, self.iteration_value

    # -- INTERNAL FUNCTIONS --

    def __generate_neighbors(self) -> list[MagicCube]:
        """
        Generates all possible neighbors (successor states).
        """
        successors: list[MagicCube] = []
        data_len = self.states[-1].size ** 3

        for x1 in range(data_len):
            for x2 in range(x1 + 1, data_len):
                cube_swap = self.states[-1].swap_index_copy(x1, x2)
                successors.append(cube_swap)

        return successors
