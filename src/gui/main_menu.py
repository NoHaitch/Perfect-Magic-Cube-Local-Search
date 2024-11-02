from gui.cube_input import CubeInput
from gui.algorithm_selection import AlgorithmSelection
from data_structure.magic_cube import MagicCube

import tkinter as tk


class MainMenu(tk.Frame):
    """
    Main Menu Window Frame.

    Calls CubeInput and AlgorithmSelection.
    """

    def __init__(self, master: tk.Tk = None):
        super().__init__(master)                   # construct main menu window
        self.master: tk.Tk = master                # Reference to the main window
        self.cube: MagicCube = MagicCube(size=5)   # Initialize the Magic Cube object

        # Title Label
        self.title_label = tk.Label(self,
                                    text="Perfect Magic Cube Solver\nusing Local Search",
                                    font=("Comic Sans MS", 20, "bold"))
        self.title_label.pack(pady=30)

        # Create input field
        self.cube_input = CubeInput(self, self.cube)
        self.cube_input.pack(pady=30, padx=50)

        # Algorithm selection
        self.algorithm_selection = AlgorithmSelection(self, self.cube)
        self.algorithm_selection.pack(pady=30, padx=50)

    def randomize_cube(self) -> None:
        """
        Randomize the cube data and update the input field.
        """
        self.cube.randomize()                           # Randomize the cube data
        self.cube_input.update_cube(self.cube.data)     # Update the input text area with the new cube data
