import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class Visualization(tk.Frame):
    def __init__(self, master, magic_cube):
        super().__init__(master)
        self.master = master
        self.magic_cube = magic_cube
        self.cube_size = magic_cube.size
        self.row_colors = ['red', 'blue', 'green', 'orange', 'purple']
        self.spacing_factor = 1.5
        self.margin_factor = 0.5

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
        self.draw_cube()

        # Embed the Matplotlib plot into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a slider to adjust the cube visualization
        self.slider = tk.Scale(
            self, from_=0, to=100, orient=tk.HORIZONTAL,
            command=lambda val: self.update_cube(int(val))
        )
        self.slider.pack(side=tk.BOTTOM)

    def draw_cube(self):
        """Draw the cube and initial visualization."""
        for i in range(len(self.x)):
            # Determine the color based on the row index (y value)
            color = self.row_colors[self.y[i] % self.cube_size]
            self.ax.text(
                self.spaced_x[i], self.spaced_y[i], self.spaced_z[i],
                str(self.magic_cube.data[i]),
                color=color, fontsize=12, ha='center', va='center', fontweight='bold'
            )

        # Set initial axis limits to create a true cube with margin
        self.ax.set_xlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_ylim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_zlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])

        # Remove grid numbers and ticks for a cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.set_zlabel('')

        # Draw the wireframe box
        self.draw_wireframe()

    def draw_wireframe(self):
        """Draw a wireframe around the cube to give a 3D box effect."""
        max_dim = (self.cube_size - 1) * self.spacing_factor
        min_coord = -self.margin_factor
        max_coord = max_dim + self.margin_factor

        # Define corners of the box
        corners = [
            (min_coord, min_coord, min_coord), (min_coord, min_coord, max_coord),
            (min_coord, max_coord, min_coord), (min_coord, max_coord, max_coord),
            (max_coord, min_coord, min_coord), (max_coord, min_coord, max_coord),
            (max_coord, max_coord, min_coord), (max_coord, max_coord, max_coord)
        ]

        # Define lines to connect corners
        lines = [
            (corners[0], corners[1]), (corners[0], corners[2]), (corners[0], corners[4]),
            (corners[1], corners[3]), (corners[1], corners[5]), (corners[2], corners[3]),
            (corners[2], corners[6]), (corners[3], corners[7]), (corners[4], corners[5]),
            (corners[4], corners[6]), (corners[5], corners[7]), (corners[6], corners[7])
        ]

        # Draw the wireframe lines
        for line in lines:
            start, end = line
            self.ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color='black')

    def update_cube(self, val):
        """Update the cube's visualization based on slider value."""
        self.ax.clear()

        # Use MagicCube's data or manipulate it based on the slider
        shifted_numbers = (self.magic_cube.data + int(val)) % 100

        # TODO: dont use random generated numbers
        for i in range(len(self.x)):
            # Determine the color based on the row index (y value)
            color = self.row_colors[self.y[i] % self.cube_size]
            self.ax.text(
                self.spaced_x[i], self.spaced_y[i], self.spaced_z[i],
                str(shifted_numbers[i]),
                color=color, fontsize=12, ha='center', va='center', fontweight='bold'
            )

        # Set axis limits again to ensure the frame remains
        self.ax.set_xlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_ylim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])
        self.ax.set_zlim([-self.margin_factor, (self.cube_size - 1) * self.spacing_factor + self.margin_factor])

        # Draw the wireframe box again
        self.draw_wireframe()

        # Redraw the updated figure
        self.canvas.draw()
