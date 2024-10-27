import tkinter as tk
from src.gui.visualization import Visualization
from src.algorithm.hc_random import RandomRestartHillClimbing  # Import the random restart hill climbing algorithm

class AlgorithmSelection(tk.Frame):
    def __init__(self, master=None, cube=None):
        super().__init__(master)
        self.master = master
        self.cube = cube

        # Label for algorithm selection
        self.label = tk.Label(self, text="Choose Algorithm:", font=("Arial", 12, "bold"))
        self.label.pack(pady=(10, 5))

        # Buttons for each algorithm
        self.algo_buttons = []

        # List of algorithms with corresponding methods
        algorithms = [
            ("Steepest Ascent Hill-Climbing", self.run_steepest_ascent_hill_climbing),
            ("Hill Climbing with Sideways Move", self.run_hill_climbing_with_sideways),
            ("Random Restart Hill Climbing", self.run_random_restart_hill_climbing),  # Our new algorithm
            ("Simulated Annealing", self.run_simulated_annealing),
            ("Genetic Algorithm", self.run_genetic_algorithm)
        ]

        # Loop to create buttons for each algorithm
        for algo_name, algo_method in algorithms:
            button = tk.Button(self, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)
            self.algo_buttons.append(button)

    # Placeholder methods for other algorithms
    def run_steepest_ascent_hill_climbing(self):
        print("Running Steepest Ascent Hill-Climbing...")
        self.show_visualization()

    def run_hill_climbing_with_sideways(self):
        print("Running Hill Climbing with Sideways Move...")
        self.show_visualization()

    def run_random_restart_hill_climbing(self):
        print("Running Random Restart Hill Climbing...")
        
        # Initialize and run the algorithm
        algo = RandomRestartHillClimbing(cube_size=self.cube.size)
        initial_state, final_state = algo.run()
        
        # Show the initial and final states in the visualization
        self.show_visualization(initial_state, final_state)

    def run_simulated_annealing(self):
        print("Running Simulated Annealing...")
        self.show_visualization()

    def run_genetic_algorithm(self):
        print("Running Genetic Algorithm...")
        self.show_visualization()

    # Method to show the visualization
    def show_visualization(self, initial_state=None, final_state=None):
        """
        Displays the initial and final states of the cube using the Visualization class.
        """
        visualization_window = tk.Toplevel(self)
        
        if initial_state:
            initial_vis = Visualization(visualization_window, initial_state)
            initial_vis.pack(fill='both', expand=True)
            initial_vis.canvas.draw()  # Draw the initial state

        if final_state:
            final_vis = Visualization(visualization_window, final_state)
            final_vis.pack(fill='both', expand=True)
            final_vis.canvas.draw()  # Draw the final state
