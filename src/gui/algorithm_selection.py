import tkinter as tk
from tkinter import messagebox
from algorithm.hc_steepest_ascent import HillClimbSteepest
from algorithm.hc_sideways_move import HillClimbSideways
from algorithm.hc_random import RandomRestartHillClimbing
from algorithm.simulated_annealing import SimulatedAnnealing
from algorithm.genetic_algorithm import GeneticAlgorithm
from algorithm.hc_stochastic import StochasticHillClimb
from gui.visualization import Visualization
from data_structure.magic_cube import MagicCube
import time


class AlgorithmSelection(tk.Frame):
    """
    Algorithm Selection Window Frame.
    Call Visualization to show the visualization window.
    """

    def __init__(self, master=None, initial_cube: MagicCube = None):
        super().__init__(master)  # Construct the algorithm selection window
        self.generic_algorithm_iteration = None
        self.population_amount = None
        self.generic_algorithm = False
        self.stuck_frequency = None
        self.data_per_iteration = None
        self.random_restart_iterations = None
        self.random_restart_amount = None
        self.hc_random_restart_input = False
        self.input_max_random_restart = None
        self.button_random_restart = None
        self.input_random_restart_iteration = None
        self.max_stochastic_iterations = None
        self.get_population_amount = None
        self.button_sideways = None
        self.input_sideways = None
        self.input_stochastic = None
        self.iteration = 0  # Number of iterations
        self.iteration_values = None
        self.master = master  # Reference to the main window
        self.cube: MagicCube = initial_cube  # Reference to the Magic Cube object
        self.cube_states: list[MagicCube] = [initial_cube]  # List of MagicCube objects
        self.time_taken: float = 0  # Time taken to solve the cube
        self.message_passed: str = ""  # Additional Message to be displayed
        self.algorithm: str = ""

        self.hc_sideways_input = False  # Flag to check if the input for Hill Climbing with Sideways Move is shown
        self.hc_stochastic_input = False  # Flag to check if the input for Stochastic Hill Climbing is shown
        # Label for algorithm selection
        self.label = tk.Label(self, text="Choose Algorithm:", font=("Arial", 12, "bold"))
        self.label.pack(pady=(0, 5))

        # Frame for top row (Hill Climbing algorithms)
        top_row_frame = tk.Frame(self)
        top_row_frame.pack(pady=(5, 5))

        # Frame for bottom row (Genetic Algorithm and Simulated Annealing)
        bottom_row_frame = tk.Frame(self)
        bottom_row_frame.pack(pady=(5, 10))

        # Frame for inputs
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=(10, 5))  # Added top and bottom padding
        # Frame for buttons (for inputs)
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=(5, 10))  # Added top and bottom padding
        # List of algorithms with corresponding methods
        algorithms_top = [
            ("Steepest Ascent Hill-Climbing", self.run_steepest_ascent_hill_climbing),
            ("Hill Climbing with Sideways Move", self.run_hill_climbing_with_sideways),
            ("Random Restart Hill Climbing", self.run_random_restart_hill_climbing),
            ("Stochastic Hill Climbing", self.run_stochastic_hill_climbing)
        ]
        algorithms_bottom = [
            ("Simulated Annealing", self.run_simulated_annealing),
            ("Genetic Algorithm", self.run_genetic_algorithm)
        ]

        # Create buttons for top row algorithms (Hill Climbing)
        for algo_name, algo_method in algorithms_top:
            button = tk.Button(top_row_frame, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)  # Keep the same horizontal padding

        # Create buttons for bottom row algorithms (Genetic and Simulated Annealing)
        for algo_name, algo_method in algorithms_bottom:
            button = tk.Button(bottom_row_frame, text=algo_name, command=algo_method, font=("Arial", 10))
            button.pack(side='left', padx=5)  # Keep the same horizontal padding

    # Placeholder methods for each algorithm
    def run_steepest_ascent_hill_climbing(self):
        self.algorithm = "Steepest Ascent Hill-Climbing"
        hc_steepest = HillClimbSteepest(self.cube)

        print("Running")

        start_time = time.time()
        self.cube_states, self.iteration = hc_steepest.hill_climb_steepest_ascent()
        end_time = time.time()

        print("Finished")

        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_hill_climbing_with_sideways(self):
        if not self.hc_sideways_input:
            self.hc_sideways_input = True

            self.label = tk.Label(self.input_frame, text="Maximum Sideways Move:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding

            self.input_sideways = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.input_sideways.pack(side=tk.LEFT)

            self.button_sideways = tk.Button(self.button_frame, text="Run Hill Climbing with Sideways Move",
                                             command=lambda: self.__run_hill_climbing_with_sideways())
            self.button_sideways.pack(side=tk.RIGHT, padx=(5, 0))  # Added left padding
        else:
            messagebox.showerror("Button Already Pressed", "Please use the button Run Hill climb with Sideways Move")

    def __run_hill_climbing_with_sideways(self):
        max_side = self.input_sideways.get()
        self.algorithm = "Hill Climbing with Sideways Move"
        hc_sideways = HillClimbSideways(max_side, self.cube)

        print("Running")

        start_time = time.time()
        self.cube_states, self.iteration = hc_sideways.hill_climb_sideways_move()
        end_time = time.time()

        print("Finished")

        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_random_restart_hill_climbing(self):
        if not self.hc_random_restart_input:
            self.hc_random_restart_input = True
            self.label = tk.Label(self.input_frame, text="Maximum Random Restart:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding
            self.input_max_random_restart = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.input_max_random_restart.pack(side=tk.LEFT)
            self.label = tk.Label(self.input_frame, text="Maximum Random Restart Iteration:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding
            self.input_random_restart_iteration = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.input_random_restart_iteration.pack(side=tk.LEFT)
            self.button_random_restart = tk.Button(self.button_frame, text="Run Hill Climbing with Sideways Move",
                                                   command=lambda: self.__run_random_restart_hill_climbing())
            self.button_random_restart.pack(side=tk.RIGHT, padx=(5, 0))  # Added left padding
        else:
            messagebox.showerror("Button Already Pressed", "Please use the button Run Hill climb with Sideways Move")

    def __run_random_restart_hill_climbing(self):
        max_restart = self.input_max_random_restart.get()
        max_restart_iteration = self.input_random_restart_iteration.get()
        self.algorithm = "Random Restart Hill Climbing"

        print("Running")

        start_time = time.time()
        hc_random = RandomRestartHillClimbing(self.cube.size, max_restart, max_restart_iteration, self.cube.data)
        self.cube_states, self.iteration, self.random_restart_iterations, self.random_restart_amount = hc_random.run()
        end_time = time.time()
        print("Finished")
        self.time_taken = (end_time - start_time) * 1000
        self.show_visualization()

    def run_stochastic_hill_climbing(self):
        if not self.hc_stochastic_input:
            self.hc_stochastic_input = True
            self.label = tk.Label(self.input_frame, text="Maximum Stochastic Iterations:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding
            self.input_stochastic = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.input_stochastic.pack(side=tk.LEFT)

            button_stochastic = tk.Button(self.button_frame, text="Run Stochastic Hill Climbing",
                                          command=lambda: self.__run_stochastic_hill_climbing())
            button_stochastic.pack(side=tk.RIGHT, padx=(5, 0))  # Added left padding
        else:
            messagebox.showerror("Button Already Pressed", "Please use the button Run Stochastic Hill Climbing")

    def __run_stochastic_hill_climbing(self):
        max_iterations = int(self.input_stochastic.get())
        self.algorithm = "Stochastic Hill Climbing"
        print("Running")
        start_time = time.time()
        hc_stochastic = StochasticHillClimb(self.cube)
        self.cube_states, self.iteration, self.iteration_values = hc_stochastic.stochastic_hill_climb(max_iterations)
        end_time = time.time()

        print("Finished")

        self.time_taken = (end_time - start_time) * 1000

        self.show_visualization()

    def run_simulated_annealing(self):
        self.algorithm = "Simulated Annealing"

        print("Running")

        start_time = time.time()
        initial_state = self.cube

        sa = SimulatedAnnealing(initial_state, self.cube.size)
        sa.simulated_annealing()
        self.cube_states = sa.get_states()
        self.data_per_iteration = sa.get_probability_per_iteration()
        self.stuck_frequency = sa.get_stuck_frequency()
        
        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        print("Finished")

        self.show_visualization()

    def run_genetic_algorithm(self):
        if not self.generic_algorithm:
            self.generic_algorithm = True

            self.label = tk.Label(self.input_frame, text="Generic Algorithm Population Amount:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding

            self.population_amount = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.population_amount.pack(side=tk.LEFT)

            self.label = tk.Label(self.input_frame, text="Generic Algorithm Iteration Amount:", font=("Arial", 10, "bold"))
            self.label.pack(side=tk.LEFT, padx=(0, 5))  # Added right padding

            self.generic_algorithm_iteration = tk.Entry(self.input_frame, width=4, bg="white", font=("Courier", 10))
            self.generic_algorithm_iteration.pack(side=tk.LEFT)

            self.button_sideways = tk.Button(self.button_frame, text="Run Hill Climbing with Sideways Move",
                                             command=lambda: self.__run_genetic_algorithm())
            self.button_sideways.pack(side=tk.RIGHT, padx=(5, 0))  # Added left padding
        else:
            messagebox.showerror("Button Already Pressed", "Please use the button Run Hill climb with Sideways Move")

    def __run_genetic_algorithm(self):
        self.algorithm = "Genetic Algorithm"

        print("Running")

        start_time = time.time()
        initial_state = self.cube

        ga = GeneticAlgorithm(initial_state, self.cube.size)
        ga.genetic_algorithm()
        self.cube_states = ga.get_states()
        self.get_population_amount = ga.get_population_amount()

        end_time = time.time()
        self.time_taken = (end_time - start_time) * 1000

        print("Finished")

        self.show_visualization()

    # Method to show the visualization
    def show_visualization(self) -> None:
        """
        Show the visualization window.
        """

        visualization_window = tk.Toplevel(self)
        visualization = Visualization(visualization_window, self.cube_states,
                                      self.time_taken, self.cube_states[-1].is_perfect(), self.message_passed,
                                      self.algorithm, self.iteration, self.iteration_values,
                                      self.random_restart_amount, self.random_restart_iterations,
                                      self.data_per_iteration, self.stuck_frequency, self.get_population_amount)
        visualization.pack(fill='both', expand=True)
