from src.data_structure.magic_cube import MagicCube

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualization(tk.Frame):
    """
    Visualization Window Frame. Visualize the result of local search.
    """
    class Visualization(tk.Frame):
        """
        Visualization Window Frame. Visualize the result of local search.
        """
    def __init__(self, master,
                 cube_states: list[MagicCube],
                 time_taken: float,
                 is_perfect_cube: bool,
                 message_passed: str,
                 algorithm: str,
                 iteration: int):

        super().__init__(master)                                        # Construct the visualization window
        self.master = master                                            # Reference to the main window
        self.cube_states = cube_states                                  # List of MagicCube objects
        self.cube_size = cube_states[0].size                          # Size of the cube
        self.row_colors = ['red', 'blue', 'green', 'orange', 'purple']  # Colors for each row
        self.spacing_factor = 1.5                                       # Spacing between cube elements
        self.margin_factor = 0.5                                        # Margin around the cube
        self.auto_index_slider = False
        self.iteration = iteration

        # Set the default play speed
        self.play_speed = 500
        self.current_state_index = 0

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

        # State for play/pause functionality
        self.is_playing = False

        # Create control frame for buttons
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Add Play, Pause, and Plot buttons
        self.play_button = tk.Button(control_frame, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(control_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.plot_button = tk.Button(control_frame, text="Plot", command=self.plot_cubes_and_objective)
        self.plot_button.pack(side=tk.LEFT, padx=5)

        # Create speed control buttons
        speed_frame = tk.Frame(self)
        speed_frame.pack(side=tk.BOTTOM, pady=10)

        speeds = [(0.5, 1000), (1, 500), (2, 250), (5, 100), (10, 50), (20, 25)]  # (factor, speed in ms)
        for speed_factor, speed_value in speeds:
            button = tk.Button(speed_frame, text=f"{speed_factor}x", command=lambda sv=speed_value: self.set_speed(sv))
            button.pack(side=tk.LEFT, padx=5)

        # Create a frame for the slider and buttons
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        self.left_button = tk.Button(control_frame, text="<<<", command=self.move_left100)
        self.left_button.pack(side=tk.LEFT, padx=5)

        self.left_button = tk.Button(control_frame, text="<<", command=self.move_left10)
        self.left_button.pack(side=tk.LEFT, padx=5)

        self.left_button = tk.Button(control_frame, text="<", command=self.move_left)
        self.left_button.pack(side=tk.LEFT, padx=5)

        # Create a wider slider to adjust the cube visualization
        self.slider = tk.Scale(
            control_frame, from_=0, to=len(self.cube_states) - 1, orient=tk.HORIZONTAL,
            command=self.slider_moved, length=400
        )
        self.slider.pack(side=tk.LEFT, padx=5)

        self.right_button = tk.Button(control_frame, text=">", command=self.move_right)
        self.right_button.pack(side=tk.LEFT, padx=5)

        self.right_button = tk.Button(control_frame, text=">>", command=self.move_right10)
        self.right_button.pack(side=tk.LEFT, padx=5)

        self.right_button = tk.Button(control_frame, text=">>>", command=self.move_right100)
        self.right_button.pack(side=tk.LEFT, padx=5)

        # Description label for search information
        description_text = (
            "\n"
            f"Algorithm: {algorithm}\n"
            f"Time Taken: {time_taken:.2f} milliseconds\n"
            f"Perfect Magic Cube: {'Yes' if is_perfect_cube else 'No'}\n"
            f"Total States: {len(self.cube_states)}\n"
            f"Iteration: {self.iteration}\n"
            f"{message_passed}"
            "\n"
        )
        self.description_label = tk.Label(self, text=description_text, font=("Arial", 10), justify=tk.LEFT,
                                          bg="white", borderwidth=2, relief=tk.SUNKEN, padx=20)
        self.description_label.place(relx=0, rely=0, anchor=tk.NW)  # Position at top left

        # Label to display current state value
        self.state_value_label = tk.Label(self, text="", font=("Arial", 12), justify=tk.CENTER)
        self.state_value_label.pack(pady=(5, 10), side=tk.BOTTOM)

        # Initialize state value display
        self.update_state_value(0)

    def plot_cubes_and_objective(self) -> None:
        """
        Create a new window to display the initial and resulting cubes
        and a line plot of the objective function values for each state.
        """
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Cube and Objective Function Plot")

        # Create a frame for the cubes
        cube_frame = tk.Frame(plot_window)
        cube_frame.pack(pady=10)

        # Display the initial cube
        initial_cube_label = tk.Label(cube_frame, text="Initial Cube:")
        initial_cube_label.pack()

        initial_cube_text = str(self.cube_states[0].data)  # Assuming MagicCube has a 'data' attribute
        initial_cube_display = tk.Label(cube_frame, text=initial_cube_text)
        initial_cube_display.pack()

        # Display the resulting cube
        resulting_cube_label = tk.Label(cube_frame, text="Resulting Cube:")
        resulting_cube_label.pack()

        resulting_cube_text = str(self.cube_states[-1].data)  # Last index for resulting cube
        resulting_cube_display = tk.Label(cube_frame, text=resulting_cube_text)
        resulting_cube_display.pack()

        # Prepare data for the line plot
        objective_values = [cube.get_state_value() for cube in self.cube_states]  # Assuming a method for the objective value
        iterations = list(range(len(objective_values)))

        # Create a figure for the line plot
        fig, ax = plt.subplots()
        ax.plot(iterations, objective_values, marker='o')
        ax.set_title('Objective Function Value Over Iterations')
        ax.set_xlabel('Iteration Number')
        ax.set_ylabel('Objective Value')
        ax.grid()

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add a button to close the plot window
        close_button = tk.Button(plot_window, text="Close", command=plot_window.destroy)
        close_button.pack(pady=5)

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
        self.update_state_value(val)

    def update_state_value(self, state_index) -> None:
        """
        Update the label with the current state value.
        """
        current_cube = self.cube_states[state_index]
        state_value = current_cube.get_state_value()  # Get the state value
        self.state_value_label.config(text=f"Current State Value: {state_value}")

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

    def move_left(self) -> None:
        """
        Move the slider left (to the previous state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value > 0:
            self.slider.set(current_value - 1)
            self.update_cube(current_value - 1)

    def move_right(self) -> None:
        """
        Move the slider right (to the next state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value < len(self.cube_states) - 1:
            self.slider.set(current_value + 1)
            self.update_cube(current_value + 1)

    def move_left10(self) -> None:
        """
        Move the slider left (to the previous state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value > 10:
            self.slider.set(current_value - 10)
            self.update_cube(current_value - 10)
        else:
            self.slider.set(0)
            self.update_cube(0)

    def move_right10(self) -> None:
        """
        Move the slider left (to the previous state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value < len(self.cube_states) - 10:
            self.slider.set(current_value + 10)
            self.update_cube(current_value + 10)
        else:
            self.slider.set(len(self.cube_states) - 1)
            self.update_cube(len(self.cube_states) - 1)

    def move_left100(self) -> None:
        """
        Move the slider left (to the previous state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value > 100:
            self.slider.set(current_value - 100)
            self.update_cube(current_value - 100)
        else:
            self.slider.set(0)
            self.update_cube(0)

    def move_right100(self) -> None:
        """
        Move the slider left (to the previous state) and update visualization.
        """
        current_value = self.slider.get()
        if current_value < len(self.cube_states) - 100:
            self.slider.set(current_value + 100)
            self.update_cube(current_value + 100)
        else:
            self.slider.set(len(self.cube_states) - 1)
            self.update_cube(len(self.cube_states) - 1)

    def play(self):
        """
        Start automatic update of the cube states.
        """
        self.is_playing = True
        self.update_cube(self.current_state_index)
        self.auto_update()

    def pause(self):
        """
        Stop the automatic update of the cube states.
        """
        self.is_playing = False
        self.slider.set(self.current_state_index)

    def slider_moved(self, val):
        """
        Handle slider movement.
        """
        self.update_cube(int(val))
        self.current_state_index = int(val)

    def auto_update(self):
        """
        Automatically update the cube state.
        """
        if self.is_playing:
            self.current_state_index += 1
            if self.current_state_index >= len(self.cube_states):
                self.current_state_index = 0

            # Update the cube and the slider
            self.update_cube(self.current_state_index)

            self.slider.set(self.current_state_index)

            self.after(self.play_speed, self.auto_update)

    def set_speed(self, speed_value: int) -> None:
        """
        Set the playing speed for the automatic update.
        """
        self.play_speed = speed_value
