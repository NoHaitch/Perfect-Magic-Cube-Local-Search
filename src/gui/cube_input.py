from src.data_structure.magic_cube import MagicCube

import tkinter as tk
from tkinter import messagebox
import numpy as np


class CubeInput(tk.Frame):
    """
    Cube Input Frame
    """

    def __init__(self, master=None, cube: MagicCube = None):
        super().__init__(master)        # Construct the cube input frame
        self.master = master            # Reference to the main window
        self.cube: MagicCube = cube     # Reference to the MagicCube object

        # Add a label for the input field
        self.label = tk.Label(self, text="Enter 125 comma-separated values:", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, columnspan=5, pady=(10, 5))

        # Create a large input area
        self.input_text = tk.Text(self, height=10, width=70, padx=10, pady=10, bg="white", font=("Courier", 10))
        self.input_text.grid(row=1, column=0, columnspan=5, pady=(0, 10))

        # Create the "Update Cube" button
        self.update_button = tk.Button(self, text="Update Cube", command=self.parse_input)
        self.update_button.grid(row=2, column=1, pady=10)

        # Create the "OR" label
        self.or_label = tk.Label(self, text="OR")
        self.or_label.grid(row=2, column=2, padx=10)

        # Create the "Randomize" button
        self.randomize_button = tk.Button(self, text="Randomize", command=self.randomize_data)
        self.randomize_button.grid(row=2, column=3, pady=10)

    def parse_input(self) -> None:
        """
        Parse the input text area and update the cube's data.
        """
        input_data: str = self.input_text.get("1.0", tk.END).strip()
        values: list[str] = input_data.split(',')

        # Validate the input length
        if len(values) != 125:
            messagebox.showerror("Input Error", "Please provide exactly 125 comma-separated values.")
            return

        # Try to convert values to integers
        try:
            values: list[int] = [int(v.strip()) for v in values]
        except ValueError:
            messagebox.showerror("Input Error", "All values must be integers.")
            return

        # Update the cube's data
        self.cube.data = values

        # Update the input text area with formatted data
        formatted_data = ', '.join(map(str, values))
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, formatted_data)

    def randomize_data(self) -> None:
        """
        Randomize the cube data. Called when button "Randomize" is pressed
        """
        self.master.randomize_cube()

    def update_cube(self, cube_data: np.ndarray) -> None:
        """
        Update the input area with the provided cube data.
        :param cube_data:
        """
        formatted_data = ', '.join(map(str, cube_data))
        self.input_text.delete("1.0", tk.END)  # Clear the text area
        self.input_text.insert(tk.END, formatted_data)  # Insert updated data
