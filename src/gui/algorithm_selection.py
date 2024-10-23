import tkinter as tk
from src.gui.visualization import Visualization

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
            ("Random Restart Hill Climbing", self.run_random_restart_hill_climbing),
            ("Simulated Annealing", self.run_simulated_annealing),
            ("Genetic Algorithm", self.run_genetic_algorithm)
        ]

        # Loop to create buttons for each algorithm
        for algo_name, algo_method in algorithms:
            # Using a monospaced font for the button labels
            button = tk.Button(self, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)
            self.algo_buttons.append(button)

    # Placeholder methods for each algorithm
    def run_steepest_ascent_hill_climbing(self):
        print("Running Steepest Ascent Hill-Climbing...")
        # TODO: Implement Steepest Ascent Hill-Climbing logic
        self.show_visualization()

    def run_hill_climbing_with_sideways(self):
        print("Running Hill Climbing with Sideways Move...")
        # TODO: Implement Hill Climbing with Sideways Move logic
        self.show_visualization()

    def run_random_restart_hill_climbing(self):
        print("Running Random Restart Hill Climbing...")
        # TODO: Implement Random Restart Hill Climbing logic
        self.show_visualization()

    def run_simulated_annealing(self):
        print("Running Simulated Annealing...")
        # TODO: Implement Simulated Annealing logic
        self.show_visualization()

    def run_genetic_algorithm(self):
        print("Running Genetic Algorithm...")
        # TODO: Implement Genetic Algorithm logic
        self.show_visualization()

    # Method to show the visualization
    def show_visualization(self):
        # Display the result in a 3D visualization
        visualization_window = tk.Toplevel(self)
        visualization = Visualization(visualization_window, self.cube)
        visualization.pack(fill='both', expand=True)
