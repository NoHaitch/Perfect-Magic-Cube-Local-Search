import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.data_structure.magic_cube import MagicCube
from objective_function import objective_function
import matplotlib.pyplot as plt
import copy
import time
import numpy as np

class hill_climb_random_restart:
    """
    A local search algorithm with Random Restart: Hill-Climbing with Random Restart.

    :var size: The size of the magic cube (default is 5)
    :var restarts: The number of random restarts (default is 10)
    :var max_restarts: The maximum allowed restarts to stop the search when reached.
    """
    def __init__(self, size=5, restarts=10, max_restarts=50):
        """
        Initializes the Magic Cube and objective function class with a specified number of restarts.

        :param size: Magic cube dimensions, default = 5
        :param restarts: Number of random restarts, default = 10
        :param max_restarts: Maximum allowed restarts, default = 50
        """
        self.size = size
        self.restarts = restarts
        self.max_restarts = max_restarts
        self.best_state = None
        self.best_value = -np.inf
        self.best_iteration = 0
        self.total_duration = 0

    def plot_hc_random_restart(self, all_object_values):
        """
        Returns a plot of objective function values for each restart.

        :param all_object_values: List of arrays containing objective values from each restart
        :return: Plot of objective function values
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        for i, obj_values in enumerate(all_object_values):
            ax.plot(np.arange(len(obj_values)), obj_values, label=f"Restart {i + 1}")
        
        ax.set_title("HC Random Restart Objective Function", fontsize=20, weight="bold")
        ax.set_xlabel("Iteration", fontsize=15)
        ax.set_ylabel("Objective Function Value", fontsize=15)
        ax.legend()
        ax.tick_params(labelsize=15)
        ax.grid()
        plt.close()
        
        return fig

    def hill_climb_random_restart(self):
        """
        Runs hill-climbing with random restart and finds the best overall state.

        :return: The best state, best objective function value, number of iterations, duration, all objective values across restarts, and best values per restart
        """
        start_time = time.time()
        all_object_values = []
        best_values_per_restart = []  # List to store best values per restart

        for restart in range(self.restarts):
            current = MagicCube(self.size)                     # Initialize a new random Magic Cube
            obj_func = objective_function(current)             # Initialize objective function
            current_value = obj_func.get_object_value()        # Current objective function value
            object_values = [current_value]                    # Track objective values for this restart
            iteration = 0

            # Hill-Climbing Steepest Ascent
            while True:
                neighbour, neighbour_value = self.__find_neighbour(current)

                if neighbour_value <= current_value:
                    # If no better neighbor, store this restart's objective values
                    all_object_values.append(np.array(object_values))
                    best_values_per_restart.append(current_value)  # Save the best value for this restart
                    
                    # Update best state across restarts if needed
                    if current_value > self.best_value:
                        self.best_value = current_value
                        self.best_state = copy.deepcopy(current)
                        self.best_iteration = iteration
                    
                    break  # Exit this restart when local optimum is reached

                # Update current state to the better neighbor
                current = neighbour
                current_value = neighbour_value
                object_values.append(current_value)
                iteration += 1

        self.total_duration = time.time() - start_time

        return self.best_state, self.best_value, self.best_iteration, self.total_duration, all_object_values, best_values_per_restart

    # -- INTERNAL FUNCTIONS --

    def __swap(self, cube, x1, x2):
        """
        Swap two elements in the cube data and return the new state.

        :param cube: A magic cube class
        :param x1: First target index
        :param x2: Second target index
        :return: A swapped magic cube state
        """
        cube_swap = copy.deepcopy(cube)
        cube_swap.data[[x1, x2]] = cube_swap.data[[x2, x1]]
        return cube_swap
    
    def __find_neighbour(self, cube):
        """
        Returns the best state and its objective function value by swapping two different positions.

        :param cube: A magic cube class
        :return: The best state and its objective function value
        """
        successors = []
        object_successors = []
        for x1 in range(len(cube.data)):
            for x2 in range(x1 + 1, len(cube.data)):  # Ensure x1 and x2 are different
                cube_swap = self.__swap(cube, x1, x2)
                object_value = objective_function(cube_swap).get_object_value()
                successors.append(cube_swap)
                object_successors.append(object_value)

        best_index = np.argmax(object_successors)
        return successors[best_index], object_successors[best_index]

