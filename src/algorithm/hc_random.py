import numpy as np
from src.data_structure.magic_cube import MagicCube
from src.algorithm.objective_function import ObjectiveFunction
import copy
from random import randint
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class RandomRestartHillClimbing:
    def __init__(self, cube_size=5, max_restarts=10, max_iterations=20, initial_state=None):
        """
        Initializes the algorithm with a magic cube of specified size and limits on restarts and iterations.
        
        :param cube_size: The size of the cube (default is 5 for a 5x5x5 cube).
        :param max_restarts: The maximum number of random restarts.
        :param max_iterations: The maximum number of iterations per restart.
        :param initial_state: Optional initial state for the cube.
        """
        self.cube_size = cube_size
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        self.best_cube = None
        self.best_score = float('inf')
        self.objective_values = []  # Store objective values for plotting

        # Initialize cube state
        self.initial_cube = MagicCube(size=self.cube_size)
        if initial_state is not None:  # Check if initial_state is provided
            self.initial_cube.data = initial_state

    def evaluate(self, cube):
        """
        Evaluates the cube using the objective function value.
        
        :param cube: An instance of MagicCube.
        :return: An integer score representing the cube's fitness (lower is better).
        """
        return ObjectiveFunction.get_object_value(cube)

    def swap_elements(self, cube):
        idx1, idx2 = randint(0, cube.size**3 - 1), randint(0, cube.size**3 - 1)
        while idx1 == idx2:
            idx2 = randint(0, cube.size**3 - 1)  # Ensure idx2 is different
        cube.data[idx1], cube.data[idx2] = cube.data[idx2], cube.data[idx1]
        return idx1, idx2
    
    def revert_swap(self, cube, idx1, idx2):
        """
        Reverts a swap of two elements within the cube data.
        
        :param cube: An instance of MagicCube.
        :param idx1: The first index used in the swap.
        :param idx2: The second index used in the swap.
        """
        cube.data[idx1], cube.data[idx2] = cube.data[idx2], cube.data[idx1]

    def run(self):
        self.best_cube = copy.deepcopy(self.initial_cube)
        self.best_score = self.evaluate(self.initial_cube)
        best_states_per_restart = []  # Track the best state of each restart
        best_scores_per_restart = []  # Track the best score of each restart
        total_iterations = 0

        for restart in range(self.max_restarts):
            cube = copy.deepcopy(self.initial_cube) if restart == 0 else MagicCube(size=self.cube_size)
            current_score = self.evaluate(cube)
            best_local_state = copy.deepcopy(cube)
            best_local_score = current_score
            iteration_scores = []

            for iteration in range(self.max_iterations):
                best_neighbor_score = current_score
                best_swap = None

                # Evaluate all neighbors by swapping pairs of elements
                for i in range(len(cube.data)):
                    for j in range(i + 1, len(cube.data)):
                        # Perform swap
                        cube.data[i], cube.data[j] = cube.data[j], cube.data[i]
                        neighbor_score = self.evaluate(cube)

                        # Track the best neighbor
                        if neighbor_score > best_neighbor_score:
                            best_neighbor_score = neighbor_score
                            best_swap = (i, j)

                        # Revert swap to try the next pair
                        cube.data[i], cube.data[j] = cube.data[j], cube.data[i]

                # If no better neighbor is found, break out of the loop
                if best_swap is None:
                    print(f"No improvement found at Restart {restart}, Iteration {iteration}. Best local score: {best_local_score}")
                    break

                # Perform the best swap
                i, j = best_swap
                cube.data[i], cube.data[j] = cube.data[j], cube.data[i]
                current_score = best_neighbor_score
                total_iterations += 1

                # Update best state for the current restart
                if current_score > best_local_score:
                    best_local_state = copy.deepcopy(cube)
                    best_local_score = current_score

                iteration_scores.append(current_score)

            # Save the best state and score for this restart
            best_states_per_restart.append(best_local_state)
            best_scores_per_restart.append(best_local_score)
            print(f"Restart {restart} completed. Best score for this restart: {best_local_score}")

        return best_states_per_restart, total_iterations
