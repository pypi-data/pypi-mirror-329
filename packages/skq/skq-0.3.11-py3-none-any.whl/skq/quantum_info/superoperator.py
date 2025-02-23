import numpy as np


class SuperOperator(np.ndarray):
    """Base class for quantum superoperators. For example quantum channels."""

    def __new__(cls, input_array: np.array):
        arr = np.array(input_array, dtype=complex)
        obj = arr.view(cls)
        assert obj.is_at_least_nxn(n=1), "Superoperator must be at least a 1x1 matrix."
        assert obj.is_power_of_n_shape(n=2), "Superoperator must have a power of 2 shape."
        return obj

    def is_at_least_nxn(self, n: int) -> bool:
        """Superoperator is at least an n x n matrix."""
        return self.shape[0] >= n and self.shape[1] >= n

    def is_power_of_n_shape(self, n: int) -> bool:
        """
        Superoperator shape is a power of n.
        :param n: Number to check for power of n shape.
        """

        def _is_power_of_n(x, n):
            if x < 1:
                return False
            while x % n == 0:
                x //= n
            return x == 1

        return _is_power_of_n(self.shape[0], n) and _is_power_of_n(self.shape[1], n)

    def conjugate_transpose(self) -> np.ndarray:
        """
        Conjugate transpose (i.e. Hermitian adjoint or 'dagger operation') of the superoperator.
        1. Transpose the matrix
        2. Take the complex conjugate of each element (Flip the sign of the imaginary part)
        """
        return self.T.conj()
