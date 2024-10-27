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
    
        # Ambil data input cube sebagai initial state dan pastikan itu berupa objek MagicCube
        initial_state = self.cube  # Asumsikan self.cube adalah instance dari MagicCube
    
        # Inisialisasi dan jalankan algoritme dengan initial state
        algo = RandomRestartHillClimbing(cube_size=self.cube.size, initial_state=initial_state.data)
        _, final_state_data, final_score, duration = algo.run()
    
        # Buat objek MagicCube baru untuk final_state
        final_state = MagicCube(size=self.cube.size)
        final_state.data = final_state_data.data  # Pastikan formatnya sesuai

        # Tampilkan visualisasi dari kondisi awal dan akhir
        self.show_visualization(initial_state=initial_state, final_state=final_state)


    def run_simulated_annealing(self):
        print("Running Simulated Annealing...")
        self.show_visualization()

    def run_genetic_algorithm(self):
        print("Running Genetic Algorithm...")
        self.show_visualization()

    def show_visualization(self, initial_state=None, final_state=None):
        """
        Displays a window with buttons to visualize either the initial or final state of the cube.
        """
        visualization_window = tk.Toplevel(self)
        visualization_window.title("Magic Cube Visualization")

        # Function to display initial condition
        def show_initial():
            # Clear previous visualization if any
            for widget in visualization_window.winfo_children():
                widget.destroy()
            # Label for Initial State
            initial_label = tk.Label(visualization_window, text="Initial State", font=("Arial", 12, "bold"))
            initial_label.pack()
            # Visualization for Initial State
            initial_vis = Visualization(visualization_window, initial_state)
            initial_vis.pack(fill='both', expand=True)
            initial_vis.canvas.draw()  # Draw the initial state
            # Buttons for switching
            show_buttons()

        # Function to display final condition
        def show_final():
            # Clear previous visualization if any
            for widget in visualization_window.winfo_children():
                widget.destroy()
            # Label for Final State
            final_label = tk.Label(visualization_window, text="Final State", font=("Arial", 12, "bold"))
            final_label.pack()
            # Visualization for Final State
            final_vis = Visualization(visualization_window, final_state)
            final_vis.pack(fill='both', expand=True)
            final_vis.canvas.draw()  # Draw the final state
            # Buttons for switching
            show_buttons()

        # Function to display buttons
        def show_buttons():
            # Button to show Initial State
            initial_button = tk.Button(visualization_window, text="Show Initial Condition", command=show_initial)
            initial_button.pack(side='left', padx=10, pady=10)
            # Button to show Final State
            final_button = tk.Button(visualization_window, text="Show Final Condition", command=show_final)
            final_button.pack(side='right', padx=10, pady=10)

        # Display initial state by default, along with the buttons
        show_initial()
