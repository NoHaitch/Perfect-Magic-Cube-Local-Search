from data_structure.magic_cube import MagicCube

import numpy as np


class HillClimbSideways:
    """
    A local search algorithm: Hill-Climbing Sideways Move.
    """
    def __init__(self, max_side, initial_cube: MagicCube):
        self.states: list[MagicCube] = [initial_cube]   # self.states[-1] is the current state
        self.max_sides: int = int(max_side)

    def hill_climb_sideways_move(self) -> tuple[list[MagicCube], int]:
        """
        Returns the best state and the amount of iterations.
        """
        current = self.states[-1].copy()                        # copy of Magic cube class initial
        current_value = current.get_state_value()               # initial state value
        i = 0                                                   # initiation the number of iterations
        i_sides = 0                                             # initiation the number of iterations with sideways move

        # Loop of hill-climbing sideways move
        while True:
            # find the best state and its value
            neighbour, neighbour_value = self.__get_highest_value_neigbour(i_sides)
            
            if (neighbour_value < current_value) or (i_sides == self.max_sides):
                # if the neighbour objective function value is LESS than the current objective function value
                # stop the local search
                return self.states, i
            
            self.states.append(neighbour)
            if neighbour_value == current_value:
                i_sides += 1
            else:
                i_sides = 0
            current_value = neighbour_value
            i += 1
            print(f"iteration {i}, sideways iteration {i_sides} - current value {current_value}")
    
    # -- INTERNAL FUNCTION --

    def __get_highest_value_neigbour(self, i_sides):
        """
        Returns the best state and its state value.
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

        max_indices = np.where(np_successors_state == np_successors_state.max())[0]                 # Get max successor value indices 
        successors_max = np.array(successors)[max_indices]                                          # Successors that have maximum state value
        successors_state_max = np_successors_state[max_indices]                                     # Successor values that have maximum state value
        i_same = []

        # Get the indices of successors that are present in the current state list
        for idx in range(len(self.states)):
            for idx_max, successor_max in enumerate(successors_max):
                if (successor_max.data == self.states[idx].data):
                    i_same.append(idx_max)

        if len(i_same) > 0:
            # Delete list of successors (with maximum state value) that are contained in the current state list 
            state_same_drop = np.delete(successors_max, i_same, axis=0) 
            state_value_same_drop = np.delete(successors_state_max, i_same, axis=0)
            
            # If there are some successors equal to the current state list
            # return the next state that has maximum state value
            return state_same_drop[0], state_value_same_drop[0]

        # Return the best successor and its state value
        return successors[max_index], successors_state[max_index]
    
