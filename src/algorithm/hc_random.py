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
        self.best_cube = copy.deepcopy(self.initial_cube)
        self.best_score = self.evaluate(self.initial_cube)
        self.best_iteration_scores = []
        best_scores_per_restart = []
        start_time = time.time()

        for restart in range(self.max_restarts):
            cube = copy.deepcopy(self.initial_cube) if restart == 0 else MagicCube(size=self.cube_size)
            current_score = self.evaluate(cube)
            iteration_scores = []

            for iteration in range(self.max_iterations):
                best_neighbor_score = current_score
                best_swap = None

                # Coba semua neighbor dengan melakukan swap setiap pasangan elemen
                for i in range(len(cube.data)):
                    for j in range(i + 1, len(cube.data)):
                        # Lakukan swap
                        cube.data[i], cube.data[j] = cube.data[j], cube.data[i]
                        neighbor_score = self.evaluate(cube)

                        # Periksa apakah ini neighbor terbaik
                        if neighbor_score > best_neighbor_score:
                            best_neighbor_score = neighbor_score
                            best_swap = (i, j)

                        # Kembalikan swap untuk coba pasangan berikutnya
                        cube.data[i], cube.data[j] = cube.data[j], cube.data[i]

                # Jika tidak ada neighbor yang lebih baik, keluar dari loop iterasi
                if best_swap is None:
                    print(f"No improvement found at Restart {restart}, Iteration {iteration}. Current best score: {current_score}")
                    break

                # Jika ada neighbor yang lebih baik, lakukan swap terbaik
                i, j = best_swap
                cube.data[i], cube.data[j] = cube.data[j], cube.data[i]
                current_score = best_neighbor_score

                if current_score > self.best_score:
                    self.best_cube = copy.deepcopy(cube)
                    self.best_score = current_score
                    self.best_iteration_scores = iteration_scores[:]
                iteration_scores.append(current_score)

            # Tambahkan skor terbaik dari setiap restart ke daftar
            best_scores_per_restart.append(current_score)
        
            # Print nilai terbaik yang dicapai pada restart ini
            print(f"Restart {restart} completed. Best score for this restart: {current_score}")

        duration = time.time() - start_time
        return self.initial_cube, self.best_cube, self.best_score, duration, self.best_iteration_scores, best_scores_per_restart


    def show_summary_window(self, final_score, duration, best_iteration_scores, best_scores_per_restart):
        """
        Creates a new window to display the summary with two side-by-side plots.
        
        :param final_score: Final objective function score achieved.
        :param duration: Duration of the search process.
        :param best_iteration_scores: List of objective values over iterations for the best restart.
        :param best_scores_per_restart: List of best scores achieved in each restart.
        """
        summary_window = tk.Toplevel()
        summary_window.title("Algorithm Summary")

        # Display Final Objective Function Value and Duration
        tk.Label(summary_window, text=f"Final Objective Function Value: {final_score}", font=("Arial", 12)).pack(pady=10)
        tk.Label(summary_window, text=f"Duration: {duration:.2f} seconds", font=("Arial", 12)).pack(pady=10)

        # Create side-by-side plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Plot di sebelah kiri: Objective Function over Iterations (Best Restart)
        ax1.plot(best_iteration_scores, label="Best Restart Objective Function")
        ax1.set_xlabel("Iterations")
        ax1.set_ylabel("Objective Function Value")
        ax1.set_title("Objective Function Value over Iterations (Best Restart)")
        ax1.legend()

        # Plot di sebelah kanan: Best Scores per Restart
        ax2.plot(best_scores_per_restart, label="Best Score per Restart", color='orange')
        ax2.set_xlabel("Restarts")
        ax2.set_ylabel("Objective Function Value")
        ax2.set_title("Best Objective Function Value per Restart")
        ax2.legend()

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