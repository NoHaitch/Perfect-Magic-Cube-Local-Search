from src.data_structure.magic_cube import MagicCube

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualization(tk.Frame):
    """
    Visualization Window Frame. Visualize the result of local search.
    """
    def __init__(self, master, cube_states: list[MagicCube]):
        super().__init__(master)                                        # Construct the visualization window
        self.master = master                                            # Reference to the main window
        self.cube_states = cube_states                                  # List of MagicCube objects
        self.cube_size = cube_states[0].size                            # Size of the cube
        self.row_colors = ['red', 'blue', 'green', 'orange', 'purple']  # Colors for each row
        self.spacing_factor = 1.5                                       # Spacing between cube elements
        self.margin_factor = 0.5                                        # Margin around the cube

        # Create 3D figure with Matplotlib
        self.fig = plt.Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Initialize cube positions
        x, y, z = np.meshgrid(
            np.arange(self.cube_size),
            np.arange(self.cube_size),
            np.arange(self.cube_size)
        )
        self.x, self.y, self.z = x.flatten(), y.flatten(), z.flatten()

        # Apply spacing factor
        self.spaced_x = self.x * self.spacing_factor
        self.spaced_y = self.y * self.spacing_factor
        self.spaced_z = self.z * self.spacing_factor

        # Draw the initial cube visualization
        self.draw_cube(0)

        # Embed the Matplotlib plot into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a slider to adjust the cube visualization
        self.slider = tk.Scale(
            self, from_=0, to=len(self.cube_states) - 1, orient=tk.HORIZONTAL,
            command=lambda val: self.update_cube(int(val))
        )
        self.slider.pack(side=tk.BOTTOM)

        # Buttons for initial and end states
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM)

        self.init_button = tk.Button(button_frame, text="Initial State", command=self.show_initial_state)
        self.init_button.pack(side=tk.LEFT, padx=5)

        self.end_button = tk.Button(button_frame, text="End State", command=self.show_end_state)
        self.end_button.pack(side=tk.RIGHT, padx=5)

    def draw_cube(self, state_index) -> None:
        """
        Draw the cube at a specific state index.
        """
        self.ax.clear()
        cube_state = self.cube_states[state_index].data

        for i in range(len(self.x)):
            # Determine the color based on the row index (y value)
            color = self.row_colors[self.y[i] % self.cube_size]
            self.ax.text(
                self.spaced_x[i], self.spaced_y[i], self.spaced_z[i],
                str(cube_state[i]),
                color=color, fontsize=12, ha='center', va='center', fontweight='bold'
            )

        # Set axis limits
        self.ax.set_xlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_ylim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_zlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])

        # Draw the wireframe box
        self.draw_wireframe()

    def draw_wireframe(self) -> None:
        """
        Draw a wireframe around the cube to give a 3D box effect.
        """
        max_dim = (self.cube_size - 1) * self.spacing_factor
        min_coord = -self.margin_factor
        max_coord = max_dim + self.margin_factor

        corners = [
            (min_coord, min_coord, min_coord), (min_coord, min_coord, max_coord),
            (min_coord, max_coord, min_coord), (min_coord, max_coord, max_coord),
            (max_coord, min_coord, min_coord), (max_coord, min_coord, max_coord),
            (max_coord, max_coord, min_coord), (max_coord, max_coord, max_coord)
        ]

        lines = [
            (corners[0], corners[1]), (corners[0], corners[2]), (corners[0], corners[4]),
            (corners[1], corners[3]), (corners[1], corners[5]), (corners[2], corners[3]),
            (corners[2], corners[6]), (corners[3], corners[7]), (corners[4], corners[5]),
            (corners[4], corners[6]), (corners[5], corners[7]), (corners[6], corners[7])
        ]

        for line in lines:
            start, end = line
            self.ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color='black')

    def update_cube(self, val) -> None:
        """
        Update the cube's visualization based on slider value.
        """
        self.draw_cube(val)
        self.canvas.draw()

    def show_initial_state(self) -> None:
        """
        Set slider to the initial state and update visualization.
        """
        self.slider.set(0)
        self.update_cube(0)

    def show_end_state(self) -> None:
        """
        Set slider to the end state and update visualization.
        """
        last_index = len(self.cube_states) - 1
        self.slider.set(last_index)
        self.update_cube(last_index)
