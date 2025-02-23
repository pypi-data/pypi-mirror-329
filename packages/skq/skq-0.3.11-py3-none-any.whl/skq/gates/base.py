import numpy as np
from ..base import Operator


class BaseGate(Operator):
    """
    Base class for quantum gates of any computational basis.
    The gate must be a 2D unitary matrix.
    :param input_array: Input array to create the gate. Will be converted to a NumPy array.
    """

    def __new__(cls, input_array) -> "BaseGate":
        obj = super().__new__(cls, input_array)
        assert obj.is_unitary(), "Gate must be unitary."
        return obj

    def is_unitary(self) -> bool:
        """Check if the gate is unitary (U*U^dagger = I)"""
        identity = np.eye(self.shape[0])
        return np.allclose(self @ self.conjugate_transpose(), identity)

    def kernel_density(self, other: "BaseGate") -> complex:
        """
        Calculate the quantum kernel using density matrices.
        The kernel is defined as Tr(U * V).
        :param other: Gate object to compute the kernel with.
        :return kernel: Complex number representing the kernel density.
        """
        assert isinstance(other, BaseGate), "Other object must be an instance of BaseUnitary (i.e. a Unitary matrix)."
        assert self.num_levels() == other.num_levels(), "Gates must have the same number of rows for the kernel density."
        return np.trace(self @ other)

    def hilbert_schmidt_inner_product(self, other: "BaseGate") -> complex:
        """
        Calculate the Hilbert-Schmidt inner product with another gate.
        The inner product is Tr(U^dagger * V).
        :param other: Gate object to compute the inner product with.
        :return inner_product: Complex number representing the inner product.
        """
        assert isinstance(other, BaseGate), "Other object must be an instance of BaseUnitary (i.e. a Unitary matrix)."
        assert self.num_levels() == other.num_levels(), "Gates must have the same number of rows for the Hilbert-Schmidt inner product."
        return np.trace(self.conjugate_transpose() @ other)

    def convert_endianness(self) -> "BaseGate":
        """Convert a gate matrix from big-endian to little-endian and vice versa."""
        num_qubits = self.num_qubits
        perm = np.argsort([int(bin(i)[2:].zfill(num_qubits)[::-1], 2) for i in range(2**num_qubits)])
        return self[np.ix_(perm, perm)]
