import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tkinter as tk
from src.gui.cube_input import CubeInput
from src.gui.algorithm_selection import AlgorithmSelection
from src.data_structure.magic_cube import MagicCube

class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.cube = MagicCube(size=5)  # Initialize the Magic Cube object

        # Title Label
        self.title_label = tk.Label(self, text="Perfect Magic Cube Solver\nusing Local Search", font=("Comic Sans MS", 20, "bold"))
        self.title_label.pack(pady=30)  # Add some padding around the title

        # Create input field
        self.cube_input = CubeInput(self, self.cube)
        self.cube_input.pack(pady=30, padx=50)  # Increased horizontal padding

        # Algorithm selection
        self.algorithm_selection = AlgorithmSelection(self, self.cube)
        self.algorithm_selection.pack(pady=30, padx=50)  # Increased horizontal padding

    def randomize_cube(self):
        self.cube.randomize()  # Randomize the cube data
        self.cube_input.update_cube(self.cube.data)  # Update the input text area with the new cube data
