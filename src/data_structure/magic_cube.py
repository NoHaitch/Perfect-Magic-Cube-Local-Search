import numpy as np


class MagicCube:
    """
    A Magic Cube represented by a 1D array

    :var size: The dimensions of the Magic Cube, default is 5
    :var data: The 1D array representing the Magic Cube
    :var magic_sum: The magic number/constant for the Magic Cube
    """

    def __init__(self, size=5):
        """
        Generates a Magic Cube in the form of a 1D array with elements from 1 to 125.

        :param size: Magic Cube Dimensions, default = 5
        """
        self.size: int = size                                                       # dimensions, default 5x5x5
        # self.data: np.ndarray = np.random.permutation(np.arange(1, size**3 + 1))    # default is 1 to 125
        self.magic_sum: int = size * (size**3 + 1) // 2                             # default is 315
        self.data: np.ndarray = np.arange(1, size**3 + 1)
        # magic_sum is the magic number/constant

    def __str__(self):
        """
        Returns a string representation of the Magic Cube.
        """
        return self.data.reshape(self.size, self.size, self.size).__str__()

    def _get_index(self, x: int, y: int, z: int) -> int:
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

    def get_row(self, y: int, z: int) -> np.ndarray:
        """
        Returns the specified row.

        :return: The row at y and z
        """
        first_index = self._get_index(0, y, z)
        return self.data[first_index:first_index+self.size]

    def get_col(self, x: int, z: int) -> np.ndarray:
        """
        Returns the specified column.

        :param x: The column index.
        :param z: The layer index.
        :return: The column at x and z.
        """
        # Calculate the starting index of the specified column in the given layer
        start_index = self._get_index(x, 0, z)
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
                diagonal[i] = self.data[self._get_index(i, i, i)]
            elif start_from_left and not start_from_front:
                # From (0, n-1, 0) to (n-1, 0, n-1)
                diagonal[i] = self.data[self._get_index(i, self.size - 1 - i, i)]
            elif not start_from_left and start_from_front:
                # From (n-1, 0, 0) to (0, n-1, n-1)
                diagonal[i] = self.data[self._get_index(self.size - 1 - i, i, i)]
            else:
                # From (n-1, n-1, 0) to (0, 0, n-1)
                diagonal[i] = self.data[self._get_index(self.size - 1 - i, self.size - 1 - i, i)]

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

    # TODO: Get Side Diagonal for each axis

    # TODO: is_perfect(self) -> bool:
