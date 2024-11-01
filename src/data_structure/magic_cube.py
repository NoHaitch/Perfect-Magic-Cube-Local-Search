from src.algorithm.objective_function import ObjectiveFunction

import copy
import numpy as np


class MagicCube:
    """
    A Magic Cube represented by a 1D array

    :var size: The dimensions of the Magic Cube, default is 5
    :var data: The 1D array representing the Magic Cube
    :var magic_sum: The magic number/constant for the Magic Cube
    """

    def __init__(self, size=5, data=None):
        """
        Generates a Magic Cube in the form of a 1D array with elements from 1 to 125.

        :param size: Magic Cube Dimensions, default = 5
        """
        self.size: int = size  # dimensions, default 5x5x5
        self.data: np.ndarray = data if data is not None else np.random.permutation(np.arange(1, size**3 + 1))
        self.magic_sum: int = size * (size**3 + 1) // 2  # default is 315

    def __str__(self):
        """
        Returns a string representation of the Magic Cube.
        """
        return self.data.reshape(self.size, self.size, self.size).__str__()

    def copy(self) -> 'MagicCube':
        """
        Creates a deep copy of the current MagicCube instance.

        :return: A new MagicCube instance that is a deep copy of this instance.
        """
        return copy.deepcopy(self)

    def randomize(self) -> None:
        """
        Randomize the Magic Cube by shuffling the 1D array.
        """
        np.random.shuffle(self.data)

    def swap_coordinates(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        """
        Swap two elements in the Magic Cube at the specified coordinates
        """
        index1 = self.__get_index(x1, y1, z1)
        index2 = self.__get_index(x2, y2, z2)

        # Swap the elements
        self.data[index1], self.data[index2] = self.data[index2], self.data[index1]

    def swap_coordinates_new(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> 'MagicCube':
        """
        Swap two elements in the Magic Cube at the specified coordinates
        """
        new_cube = self.copy()
        new_cube.swap_coordinates(x1, y1, z1, x2, y2, z2)
        return new_cube

    def swap_index(self, i1, i2):
        """
        Swap two elements in the Magic Cube at the specified indices
        """
        self.data[i1], self.data[i2] = self.data[i2], self.data[i1]

    def swap_index_copy(self, i1, i2) -> 'MagicCube':
        """
        Returns a new Magic Cube with two elements swapped at the specified indices.
        """
        new_cube = self.copy()
        new_cube.swap_index(i1, i2)
        return new_cube

    def get_state_value(self):
        """
        Returns the value of the current state of the Magic Cube.
        """
        return ObjectiveFunction.get_object_value(self)

    def get_row(self, y: int, z: int) -> np.ndarray:
        """
        Returns the specified row.

        :return: The row at y and z
        """
        first_index = self.__get_index(0, y, z)
        return self.data[first_index:first_index+self.size]

    def get_col(self, x: int, z: int) -> np.ndarray:
        """
        Returns the specified column.

        :param x: The column index.
        :param z: The layer index.
        :return: The column at x and z.
        """
        # Calculate the starting index of the specified column in the given layer
        start_index = self.__get_index(x, 0, z)
        # Use slicing to return the column as a NumPy array
        return self.data[start_index:start_index + self.size**2:self.size]

    def get_pillar(self, x: int, y: int) -> np.ndarray:
        """
        Returns the specified pillar.

        :param x: The row index.
        :param y: The column index.
        :return: The vertical pillar at x and y.
        """
        # Calculate the starting index for the specified pillar
        return self.data[x + y * self.size::self.size**2]

    def get_space_diag(self, start_from_left: bool, start_from_front: bool) -> np.ndarray:
        """
        Return a space diagonal from the Magic Cube.

        :param start_from_left: true if starting from the top left of the cube
        :param start_from_front: true if starting from the top front of the cube
        :return: space diagonal from the starting point (left/right, front/back)
        """
        # Initialize the diagonal array
        diagonal = np.zeros(self.size, dtype=int)

        for i in range(self.size):
            if start_from_left and start_from_front:
                # From (0, 0, 0) to (n-1, n-1, n-1)
                diagonal[i] = self.data[self.__get_index(i, i, i)]
            elif start_from_left and not start_from_front:
                # From (0, n-1, 0) to (n-1, 0, n-1)
                diagonal[i] = self.data[self.__get_index(i, self.size - 1 - i, i)]
            elif not start_from_left and start_from_front:
                # From (n-1, 0, 0) to (0, n-1, n-1)
                diagonal[i] = self.data[self.__get_index(self.size - 1 - i, i, i)]
            else:
                # From (n-1, n-1, 0) to (0, 0, n-1)
                diagonal[i] = self.data[self.__get_index(self.size - 1 - i, self.size - 1 - i, i)]

        return diagonal

    def get_space_diags(self) -> np.ndarray:
        """
        Return all space diagonals from the Magic Cube.

        :return: A 2D array containing all space diagonals.
        """
        diagonals = [self.get_space_diag(start_from_left=True, start_from_front=True),
                     self.get_space_diag(start_from_left=True, start_from_front=False),
                     self.get_space_diag(start_from_left=False, start_from_front=True),
                     self.get_space_diag(start_from_left=False, start_from_front=False)]

        return np.array(diagonals)

    def get_side_diags_x(self) -> np.ndarray:
        """
        Return all side diagonals from the Magic Cube at x-axis as a 2D array.
        """
        left_diags = [self.__get_side_diag_x_left(i) for i in range(self.size)]
        right_diags = [self.__get_side_diag_x_right(i) for i in range(self.size)]

        # Combine left and right diagonals into a single 2D array
        return np.array(left_diags + right_diags)

    def get_side_diags_y(self) -> np.ndarray:
        """
        Return all side diagonals from the Magic Cube at y-axis as a 2D array.
        """
        left_diags = [self.__get_side_diag_y_left(i) for i in range(self.size)]
        right_diags = [self.__get_side_diag_y_right(i) for i in range(self.size)]

        return np.array(left_diags + right_diags)

    def get_side_diags_z(self) -> np.ndarray:
        """
        Return all side diagonals from the Magic Cube at z-axis as a 2D array.
        """
        left_diags = [self.__get_side_diag_z_left(i) for i in range(self.size)]
        right_diags = [self.__get_side_diag_z_right(i) for i in range(self.size)]

        return np.array(left_diags + right_diags)

    def is_perfect(self) -> bool:
        """
        Checks if the Magic Cube is a perfect magic cube.

        A perfect magic cube has the same magic sum for:
            - All rows
            - All columns
            - All pillars
            - All space diagonals
            - All side diagonals

        :return: True if the cube is perfect, False otherwise.
        """

        # Check all rows
        for z in range(self.size):
            for y in range(self.size):
                if np.sum(self.get_row(y, z)) != self.magic_sum:
                    print("Row", y, z, "sum is", np.sum(self.get_row(y, z)), "expected", self.magic_sum)
                    return False

        # Check all columns
        for z in range(self.size):
            for x in range(self.size):
                if np.sum(self.get_col(x, z)) != self.magic_sum:
                    print("Col", x, z, "sum is", np.sum(self.get_col(x, z)), "expected", self.magic_sum)
                    return False

        # Check all pillars
        for y in range(self.size):
            for x in range(self.size):
                if np.sum(self.get_pillar(x, y)) != self.magic_sum:
                    print("Pillar", x, y, "sum is", np.sum(self.get_pillar(x, y)), "expected", self.magic_sum)
                    return False

        # Check all space diagonals
        for diag in self.get_space_diags():
            if np.sum(diag) != self.magic_sum:
                print("Space Diag", diag, "sum is", np.sum(diag), "expected", self.magic_sum)
                return False

        # Check all side diagonals on each axis
        for diag_x in self.get_side_diags_x():
            if np.sum(diag_x) != self.magic_sum:
                print("Side Diag X", diag_x, "sum is", np.sum(diag_x), "expected", self.magic_sum)
                return False

        for diag_y in self.get_side_diags_y():
            if np.sum(diag_y) != self.magic_sum:
                print("Side Diag Y", diag_y, "sum is", np.sum(diag_y), "expected", self.magic_sum)
                return False

        for diag_z in self.get_side_diags_z():
            if np.sum(diag_z) != self.magic_sum:
                print("Side Diag Z", diag_z, "sum is", np.sum(diag_z), "expected", self.magic_sum)
                return False

        # If all checks pass, it's a perfect magic cube
        return True

    # -- INTERNAL/PRIVATE FUNCTIONS --

    def __get_index(self, x: int, y: int, z: int) -> int:
        """
        Returns the 1D index for the given x, y, z coordinates in the Magic Cube.

        :return: The corresponding index in the 1D array.
        """
        if x < 0 or x >= self.size:
            raise IndexError("Row index out of bounds")
        if y < 0 or y >= self.size:
            raise IndexError("Column index out of bounds")
        if z < 0 or z >= self.size:
            raise IndexError("Layer index out of bounds")

        return x + y * self.size + z * self.size**2

    def __get_side_diag_x_left(self, x: int) -> np.ndarray:
        return np.array([self.data[self.__get_index(x, i, i)] for i in range(self.size)])

    def __get_side_diag_x_right(self, x: int) -> np.ndarray:
        return np.array([self.data[self.__get_index(x, i, self.size - 1 - i)] for i in range(self.size)])

    def __get_side_diag_y_left(self, y: int) -> np.ndarray:
        return np.array([self.data[self.__get_index(i, y, i)] for i in range(self.size)])

    def __get_side_diag_y_right(self, y: int) -> np.ndarray:
        return np.array([self.data[self.__get_index(self.size - 1 - i, y, i)] for i in range(self.size)])

    def __get_side_diag_z_left(self, z) -> np.ndarray:
        return np.array([self.data[self.__get_index(i, i, z)] for i in range(self.size)])

    def __get_side_diag_z_right(self, z) -> np.ndarray:
        return np.array([self.data[self.__get_index(i, self.size - 1 - i, z)] for i in range(self.size)])
