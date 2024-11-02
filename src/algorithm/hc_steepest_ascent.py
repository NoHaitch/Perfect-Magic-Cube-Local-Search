from src.data_structure.magic_cube import MagicCube

import numpy as np


class HillClimbSteepest:
    """`
    A local search algorithm: Hill-Climbing Steepest Ascent.
    """
    def __init__(self, initial_cube: MagicCube):
        self.states: list[MagicCube] = [initial_cube]   # self.states[-1] is the current state

    def hill_climb_steepest_ascent(self) -> tuple[list[MagicCube], int]:
        """
        Returns the best state and the amount of iterations.
        """
        current = self.states[-1].copy()            # copy of Magic cube class initial
        current_value = current.get_state_value()   # initial state value
        i = 0                                       # initiation the number of iterations

        # Loop of hill-climbing steepest ascent
        while True:
            # find the best state and its value
            neighbour, neighbour_value = self.__get_highest_value_neighbour()

            if neighbour_value <= current_value:
                # if the neighbour state value is LESS than or EQUAL to the current state value,
                # stop the local search
                return self.states, i

            self.states.append(neighbour)
            # current = neighbour --> using self.states[-1]
            current_value = neighbour_value
            i += 1
            print("iteration", i, "- current value", current_value)

    # -- INTERNAL FUNCTIONS --

    def __get_highest_value_neighbour(self):
        """
        Returns the best cube state and its state value
        """

        # Initialize arrays for successors and their state values
        successors: list[MagicCube] = []
        successors_state: list[int] = []
        data_len = self.states[-1].size ** 3

        # Generate all possible swaps and calculate their state values
        for x1 in range(data_len):
            for x2 in range(x1 + 1, data_len):
                # get successor
                cube_swap = self.states[-1].swap_index_copy(x1, x2)
                state_value = cube_swap.get_state_value()

                # add to successors list
                successors.append(cube_swap)
                successors_state.append(state_value)

        # Convert to NumPy arrays for fast indexing
        np_successors_state = np.array(successors_state)

        # Find the index of the maximum state value
        max_index = np.argmax(np_successors_state)

        # Return the best successor and its state value
        return successors[max_index], successors_state[max_index]
