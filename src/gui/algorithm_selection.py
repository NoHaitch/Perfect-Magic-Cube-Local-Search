import tkinter as tk
from src.gui.visualization import Visualization
from src.algorithm.hc_random import RandomRestartHillClimbing  # Import the random restart hill climbing algorithm
from src.data_structure.magic_cube import MagicCube

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

    # Pada saat menjalankan random restart hill climbing
    def run_random_restart_hill_climbing(self):
        print("Running Random Restart Hill Climbing...")
    
        # Dapatkan *initial state* dan jalankan algoritme
        initial_state = self.cube
        self.algo = RandomRestartHillClimbing(cube_size=self.cube.size, initial_state=initial_state.data)
        initial_cube, final_state_data, final_score, duration = self.algo.run()
    
        # Buat objek MagicCube baru untuk *final state*
        final_state = MagicCube(size=self.cube.size)
        final_state.data = final_state_data.data

        # Tampilkan ringkasan hasil dalam jendela baru
        self.algo.show_summary_window(final_score=final_score, duration=duration)
        self.show_visualization(initial_state=initial_state, final_state=final_state)

    def run_simulated_annealing(self):
        print("Running Simulated Annealing...")
        self.show_visualization()

    def run_genetic_algorithm(self):
        print("Running Genetic Algorithm...")
        self.show_visualization()

    def show_visualization(self, initial_state, final_state):
        # Jendela untuk Initial State
        initial_window = tk.Toplevel(self)
        initial_window.title("Initial State Visualization")
    
        initial_label = tk.Label(initial_window, text="Initial State", font=("Arial", 12, "bold"))
        initial_label.pack()
        initial_vis = Visualization(initial_window, initial_state)
        initial_vis.pack(fill='both', expand=True)
        initial_vis.canvas.draw()  # Gambar initial state

        # Jendela untuk Final State
        final_window = tk.Toplevel(self)
        final_window.title("Final State Visualization")
    
        final_label = tk.Label(final_window, text="Final State", font=("Arial", 12, "bold"))
        final_label.pack()
        final_vis = Visualization(final_window, final_state)
        final_vis.pack(fill='both', expand=True)
        final_vis.canvas.draw()  # Gambar final state
