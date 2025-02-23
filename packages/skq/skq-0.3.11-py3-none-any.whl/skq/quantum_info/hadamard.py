import numpy as np
from itertools import permutations, product

from ..base import Operator


class HadamardMatrix(Operator):
    """Hadamard matrix representation."""

    def __new__(cls, input_array: np.array):
        obj = super().__new__(cls, input_array)
        obj = np.real(obj).astype(int)
        assert obj.is_binary(), "Hadamard matrix must have entries of +1 or -1."
        assert obj.is_orthogonal(), "Hadamard matrix must have orthogonal rows and columns."
        assert obj.is_hadamard_order(), "The order of a Hadamard matrix must be 1, 2, or a multiple of 4."
        return obj

    def is_binary(self) -> bool:
        """All elements are +1 or -1."""
        return np.all(np.isin(self, [1, -1]))

    def is_orthogonal(self) -> bool:
        """Rows and columns are orthogonal."""
        n = self.shape[0]
        return np.allclose(self @ self.T, n * np.eye(n))

    def is_hadamard_order(self) -> bool:
        """Order of the Hadamard matrix is 1, 2, or a multiple of 4."""
        n = self.shape[0]
        return n == 1 or n == 2 or (n % 4 == 0)

    def determinant(self) -> float:
        """Determinant of the Hadamard matrix."""
        return np.linalg.det(self)

    def equivalence(self, other: "HadamardMatrix") -> bool:
        """Hadamard matrices are equivalent if row/column permutations and sign flips are equal."""
        permuted_matrices = self.permutations_and_sign_flips()
        return any(np.array_equal(matrix, other) for matrix in permuted_matrices)

    def spectral_norm(self) -> float:
        """Spectral norm of the Hadamard matrix.
        :return: largest singular value (i.e. spectral norm) of the Hadamard matrix.
        """
        return np.linalg.norm(self, ord=2)

    def permutations_and_sign_flips(self) -> list[np.array]:
        """Generate all matrix permutations by permuting rows/columns and flipping signs."""
        n = self.shape[0]
        matrices = []
        for row_perm in permutations(range(n)):
            for col_perm in permutations(range(n)):
                permuted_matrix = self[row_perm, :][:, col_perm]
                for signs in product([-1, 1], repeat=n):
                    sign_matrix = np.diag(signs)
                    matrices.append(sign_matrix @ permuted_matrix @ sign_matrix)
        return matrices


def generate_hadamard_matrix(order: int) -> HadamardMatrix:
    """
    Hadamard matrix of the given order using Sylvester's construction method.
    :param order: The order of the Hadamard matrix. Must be a power of 2.
    :return: HadamardMatrix of the specified order.
    """
    assert order >= 1 and (order & (order - 1)) == 0, "Order must be a power of 2."

    # Recurse block matrices to construct Hadamard matrix
    if order == 2:
        matrix = np.array([[1, 1], [1, -1]])
    else:
        H_prev = generate_hadamard_matrix(order // 2)
        matrix = np.block([[H_prev, H_prev], [H_prev, -H_prev]])
    return HadamardMatrix(matrix)
