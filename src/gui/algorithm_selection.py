from src.gui.visualization import Visualization
from src.data_structure.magic_cube import MagicCube

import tkinter as tk
import time


class AlgorithmSelection(tk.Frame):
    """
    Algorithm Selection Window Frame.

    Call Visualization to show the visualization window.
    """

    def __init__(self, master=None, initial_cube: MagicCube = None):
        super().__init__(master)                            # Construct the algorithm selection window
        self.master = master                                # Reference to the main window
        self.cube: MagicCube = initial_cube                 # Reference to the Magic Cube object
        self.cube_states: list[MagicCube] = [initial_cube]  # List of MagicCube objects
        self.time_taken: float = 0                          # Time taken to solve the cube
        self.message_passed: str = ""                       # Additional Message to be displayed
        self.algorithm: str = ""

        # Label for algorithm selection
        self.label = tk.Label(self, text="Choose Algorithm:", font=("Arial", 12, "bold"))
        self.label.pack(pady=(10, 5))

        # Frame for top row (Hill Climbing algorithms)
        top_row_frame = tk.Frame(self)
        top_row_frame.pack(pady=(5, 5))

        # Frame for bottom row (Genetic Algorithm and Simulated Annealing)
        bottom_row_frame = tk.Frame(self)
        bottom_row_frame.pack(pady=(5, 10))

        # List of algorithms with corresponding methods and frames
        algorithms_top = [
            ("Steepest Ascent Hill-Climbing", self.run_steepest_ascent_hill_climbing),
            ("Hill Climbing with Sideways Move", self.run_hill_climbing_with_sideways),
            ("Random Restart Hill Climbing", self.run_random_restart_hill_climbing)
        ]
        algorithms_bottom = [
            ("Simulated Annealing", self.run_simulated_annealing),
            ("Genetic Algorithm", self.run_genetic_algorithm)
        ]

        # Create buttons for top row algorithms (Hill Climbing)
        for algo_name, algo_method in algorithms_top:
            button = tk.Button(top_row_frame, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)

        # Create buttons for bottom row algorithms (Genetic and Simulated Annealing)
        for algo_name, algo_method in algorithms_bottom:
            button = tk.Button(bottom_row_frame, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)

    # Placeholder methods for each algorithm
    def run_steepest_ascent_hill_climbing(self):
        self.algorithm = "Steepest Ascent Hill-Climbing"
        start_time = time.time()
        self.cube_states = [MagicCube() for _ in range(10)]
        # TODO: Implement Steepest Ascent Hill-Climbing logic
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_hill_climbing_with_sideways(self):
        self.algorithm = "Hill Climbing with Sideways Move"
        start_time = time.time()
        self.cube_states = [MagicCube() for _ in range(100)]
        # TODO: Implement Hill Climbing with Sideways Move logic
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_random_restart_hill_climbing(self):
        self.algorithm = "Random Restart Hill Climbing"
        start_time = time.time()
        self.cube_states = [MagicCube() for _ in range(1000)]
        # TODO: Implement Random Restart Hill Climbing logic
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_simulated_annealing(self):
        self.algorithm = "Simulated Annealing"
        start_time = time.time()
        self.cube_states = [MagicCube() for _ in range(10000)]
        # TODO: Implement Simulated Annealing logic
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_genetic_algorithm(self):
        self.algorithm = "Genetic Algorithm"
        start_time = time.time()
        self.cube_states = [MagicCube() for _ in range(100000)]
        # TODO: Implement Genetic Algorithm logic
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    # Method to show the visualization
    def show_visualization(self) -> None:
        """
        Show the visualization window.
        """

        visualization_window = tk.Toplevel(self)
        visualization = Visualization(visualization_window, self.cube_states,
                                      self.time_taken, self.cube_states[-1].is_perfect(), self.message_passed,
                                      self.algorithm)
        visualization.pack(fill='both', expand=True)
