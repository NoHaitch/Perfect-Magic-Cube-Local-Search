import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import numpy as np
from src.data_structure.magic_cube import MagicCube
from src.algorithm.objective_function import objective_function
import copy
from random import randint

class RandomRestartHillClimbing:
    def __init__(self, cube_size=5, max_restarts=100, max_iterations=1000):
        """
        Initializes the algorithm with a magic cube of specified size and limits on restarts and iterations.
        
        :param cube_size: The size of the cube (default is 5 for a 5x5x5 cube).
        :param max_restarts: The maximum number of random restarts.
        :param max_iterations: The maximum number of iterations per restart.
        """
        self.cube_size = cube_size
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        self.best_cube = None
        self.best_score = None

    def evaluate(self, cube):
        """
        Evaluates the cube using the objective function value.
        
        :param cube: An instance of MagicCube.
        :return: An integer score representing the cube's fitness (lower is better).
        """
        return objective_function(cube).get_object_value()

    def swap_elements(self, cube):
        """
        Performs a swap of two random elements within the cube data.
        
        :param cube: An instance of MagicCube.
        """
        idx1, idx2 = randint(0, cube.size**3 - 1), randint(0, cube.size**3 - 1)
        cube.data[idx1], cube.data[idx2] = cube.data[idx2], cube.data[idx1]

    def run(self):
        """
        Runs the hill climbing algorithm with random restart.
        
        :return: The initial state and best found state of the magic cube.
        """
        initial_cube = MagicCube(size=self.cube_size)
        self.best_cube = copy.deepcopy(initial_cube)
        self.best_score = self.evaluate(initial_cube)

        for restart in range(self.max_restarts):
            cube = MagicCube(size=self.cube_size)
            current_score = self.evaluate(cube)
            
            for iteration in range(self.max_iterations):
                # Swap two elements and evaluate the new state
                self.swap_elements(cube)
                new_score = self.evaluate(cube)
                
                # Accept new state if it is better
                if new_score < current_score:
                    current_score = new_score
                    if current_score < self.best_score:
                        self.best_cube = copy.deepcopy(cube)
                        self.best_score = current_score
                else:
                    # Revert the swap if no improvement
                    self.swap_elements(cube)

                # If a perfect solution is found, exit early
                if current_score == 0:
                    print(f"Perfect solution found after {iteration} iterations in restart {restart}")
                    return initial_cube, self.best_cube

            print(f"Restart {restart} complete with best score {self.best_score}")

        return initial_cube, self.best_cube

# Example usage:
if __name__ == "__main__":
    algo = RandomRestartHillClimbing(cube_size=5)
    initial_state, final_state = algo.run()
    print("Initial State:\n", initial_state)
    print("Final State:\n", final_state)