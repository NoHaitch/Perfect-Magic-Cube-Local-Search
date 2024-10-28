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
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class RandomRestartHillClimbing:
    def __init__(self, cube_size=5, max_restarts=100, max_iterations=2000, initial_state=None):
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
        self.best_iteration_scores = []  # Menyimpan skor dari iterasi terbaik
        start_time = time.time()  # Start timing the process

        for restart in range(self.max_restarts):
            cube = copy.deepcopy(self.initial_cube) if restart == 0 else MagicCube(size=self.cube_size)
            current_score = self.evaluate(cube)
            iteration_scores = []  # Menyimpan skor setiap iterasi untuk restart ini
        
            for iteration in range(self.max_iterations):
                idx1, idx2 = self.swap_elements(cube)  # Coba melakukan swap
                new_score = self.evaluate(cube)
            
                if new_score > current_score:
                    current_score = new_score
                    if current_score > self.best_score:
                        self.best_cube = copy.deepcopy(cube)
                        self.best_score = current_score
                        # Simpan iterasi terbaik jika skor lebih tinggi dari best_score
                        self.best_iteration_scores = iteration_scores[:]
                    iteration_scores.append(current_score)
                else:
                    self.revert_swap(cube, idx1, idx2)

                if current_score >= 109:
                    print(f"Target solution reached at Restart {restart}, Iteration {iteration}")
                    self.objective_values.extend(iteration_scores)
                    end_time = time.time()
                    return self.initial_cube, self.best_cube, current_score, end_time - start_time

            self.objective_values.extend(iteration_scores)
            print(f"Restart {restart} completed with best score: {self.best_score}")

        end_time = time.time()
        return self.initial_cube, self.best_cube, self.best_score, end_time - start_time

    def show_summary_window(self, final_score, duration):
        """
        Creates a new window to display the summary of the algorithm run,
        including the final objective function value, duration, and plot.
        """
        summary_window = tk.Toplevel()
        summary_window.title("Algorithm Summary")

        # Display Final Objective Function Value
        tk.Label(summary_window, text=f"Final Objective Function Value: {final_score}", font=("Arial", 12)).pack(pady=10)

        # Display Duration
        tk.Label(summary_window, text=f"Duration: {duration:.2f} seconds", font=("Arial", 12)).pack(pady=10)

        # Plot Objective Function Over Iterations
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(self.best_iteration_scores, label="Objective Function Value")
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Objective Function Value")
        ax.set_title("Objective Function Value over Iterations")
        ax.legend()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=summary_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # Button to close the window
        close_button = tk.Button(summary_window, text="Close", command=summary_window.destroy)
        close_button.pack(pady=10)

# Example usage:
if __name__ == "__main__":
    initial_data = [randint(1, 5**3) for _ in range(5**3)]  # Example initial data
    algo = RandomRestartHillClimbing(cube_size=5, initial_state=initial_data)
    initial_state, final_state, final_score, duration = algo.run()
    print("Initial State:\n", initial_state)
    print("Final State:\n", final_state)
    print("Final Objective Function Value:", final_score)
    print("Duration of the search:", duration, "seconds")
    
    # Tampilkan grafik di jendela baru
    algo.show_graph_window()