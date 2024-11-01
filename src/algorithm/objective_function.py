from src.data_structure.magic_cube import MagicCube
import numpy as np


class ObjectiveFunction:
    """
    Objective function for local search in a magic cube.

    Static Class --> no Constructor

    Use by calling ObjectiveFunction.get_object_value: Returns objective value from internal function
    """

    @staticmethod
    def get_object_value(magic_cube: MagicCube) -> int:
        """
        Returns objective value from internal function.

        :return: Objective function value of a magic cube
        """

        # 109 is the maximum possible state value for a 5x5x5 magic cube
        return 109 - ObjectiveFunction.__check_315(magic_cube)

    @staticmethod
    def __check_315(magic_cube: MagicCube) -> int:
        """
        Returns the sum of a series (row/column/pillar/diagonal) from the cube that is not equal to the magic number.
        """

        # Check all rows
        not_315_row = 0
        for z in range(magic_cube.size):
            for y in range(magic_cube.size):
                if np.sum(magic_cube.get_row(y, z)) != magic_cube.magic_sum:
                    not_315_row += 1

        # Check all columns
        not_315_col = 0
        for z in range(magic_cube.size):
            for x in range(magic_cube.size):
                if np.sum(magic_cube.get_col(x, z)) != magic_cube.magic_sum:
                    not_315_col += 1

        # Check all pillars
        not_315_pil = 0
        for y in range(magic_cube.size):
            for x in range(magic_cube.size):
                if np.sum(magic_cube.get_pillar(x, y)) != magic_cube.magic_sum:
                    not_315_pil += 1

        # Check all space diagonals
        not_315_space_diag = 0
        for diag in magic_cube.get_space_diags():
            if np.sum(diag) != magic_cube.magic_sum:
                not_315_space_diag += 1

        # Check all side diagonals on each axis
        not_315_diag_x = 0
        for diag_x in magic_cube.get_side_diags_x():
            if np.sum(diag_x) != magic_cube.magic_sum:
                not_315_diag_x += 1

        not_315_diag_y = 0
        for diag_y in magic_cube.get_side_diags_y():
            if np.sum(diag_y) != magic_cube.magic_sum:
                not_315_diag_y += 1

        not_315_diag_z = 0
        for diag_z in magic_cube.get_side_diags_z():
            if np.sum(diag_z) != magic_cube.magic_sum:
                not_315_diag_z += 1

        return (not_315_row + not_315_col + not_315_pil + not_315_space_diag +
                not_315_diag_x + not_315_diag_y + not_315_diag_z)
