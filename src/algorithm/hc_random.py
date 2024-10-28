import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import numpy as np
from src.data_structure.magic_cube import MagicCube
from src.algorithm.objective_function import objective_function
import copy
from random import randint
import time
import matplotlib.pyplot as plt

class RandomRestartHillClimbing:
    def __init__(self, cube_size=5, max_restarts=100, max_iterations=1000, initial_state=None):
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
        return objective_function(cube).get_object_value()

    def swap_elements(self, cube):
        idx1, idx2 = randint(0, cube.size**3 - 1), randint(0, cube.size**3 - 1)
        while idx1 == idx2:
            idx2 = randint(0, cube.size**3 - 1)  # Memastikan idx2 berbeda
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
        """
        Runs the hill climbing algorithm with random restart.
    
        :return: The initial state, best found state of the magic cube, and performance details.
        """
        self.best_cube = copy.deepcopy(self.initial_cube)
        self.best_score = self.evaluate(self.initial_cube)
        start_time = time.time()  # Start timing the process

        for restart in range(self.max_restarts):
            # Mulai dengan initial cube atau random cube jika bukan restart pertama
            cube = copy.deepcopy(self.initial_cube) if restart == 0 else MagicCube(size=self.cube_size)
            current_score = self.evaluate(cube)
            iteration_scores = []  # Menyimpan skor setiap iterasi
        
            for iteration in range(self.max_iterations):
                idx1, idx2 = self.swap_elements(cube)  # Coba melakukan swap
                new_score = self.evaluate(cube)
            
                # Logging untuk melihat perubahan
                print(f"Restart {restart}, Iteration {iteration}: Current Score = {current_score}, New Score = {new_score}")

                # Terima kondisi baru jika new_score lebih tinggi dari current_score
                if new_score > current_score:
                    current_score = new_score
                    # Perbarui kondisi terbaik jika ini adalah skor tertinggi
                    if current_score > self.best_score:
                        self.best_cube = copy.deepcopy(cube)
                        self.best_score = current_score
                    iteration_scores.append(current_score)
                else:
                    # Batalkan swap jika tidak ada perbaikan
                    self.revert_swap(cube, idx1, idx2)

                # Hentikan jika skor mencapai target yang Anda anggap optimal
                if current_score >= 109:  # Contoh target nilai objektif yang dianggap sempurna
                    print(f"Target solution reached at Restart {restart}, Iteration {iteration}")
                    self.objective_values.extend(iteration_scores)
                    end_time = time.time()
                    return self.initial_cube, self.best_cube, current_score, end_time - start_time

            self.objective_values.extend(iteration_scores)
            print(f"Restart {restart} completed with best score: {self.best_score}")

        end_time = time.time()
        return self.initial_cube, self.best_cube, self.best_score, end_time - start_time


    def plot_objective_values(self):
        """
        Plots the objective function values over the course of iterations.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(self.objective_values, label="Objective Function Value")
        plt.xlabel("Iterations")
        plt.ylabel("Objective Function Value")
        plt.title("Objective Function Value over Iterations")
        plt.legend()
        plt.show()

# Example usage:
if __name__ == "__main__":
    initial_data = [randint(1, 5**3) for _ in range(5**3)]  # Example initial data
    algo = RandomRestartHillClimbing(cube_size=5, initial_state=initial_data)
    initial_state, final_state, final_score, duration = algo.run()
    print("Initial State:\n", initial_state)
    print("Final State:\n", final_state)
    print("Final Objective Function Value:", final_score)
    print("Duration of the search:", duration, "seconds")
    
    # Plot the objective function values over iterations
    algo.plot_objective_values()
