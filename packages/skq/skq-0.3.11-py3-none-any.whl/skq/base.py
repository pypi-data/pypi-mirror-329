import qiskit
import numpy as np
import pennylane as qml


class Operator(np.ndarray):
    """
    Base class for Quantum Operators.
    Gates, density matrices, hamiltonians, etc. are all operators.
    The operator must be a 2D matrix.
    :param input_array: Input array to create the operator. Will be converted to a NumPy array.
    """

    def __new__(cls, input_array):
        arr = np.asarray(input_array, dtype=complex)
        obj = arr.view(cls)
        assert obj.is_2d(), "Quantum operator must be a 2D matrix."
        assert obj.is_square(), "Quantum operator must be a square matrix."
        assert obj.is_at_least_nxn(n=1), "Gate must be at least a 1x1 matrix."
        return obj

    def encodes(self, other: np.ndarray) -> bool:
        """Progress quantum state"""
        return np.array(self @ other, dtype=complex)

    def decodes(self, other: np.ndarray) -> bool:
        """Reverse quantum state"""
        return np.array(self.conjugate_transpose() @ other, dtype=complex)

    def is_square(self) -> bool:
        """Operator is a square matrix."""
        return self.shape[0] == self.shape[1]

    def is_2d(self) -> bool:
        """Operator is a 2D matrix."""
        return len(self.shape) == 2

    def is_at_least_nxn(self, n: int) -> bool:
        """Operator is at least an n x n matrix."""
        rows, cols = self.shape
        return rows >= n and cols >= n

    def is_power_of_n_shape(self, n: int) -> bool:
        """
        Operator shape is a power of n.
        Qubits: n=2, Qutrits: n=3, Ququarts: n=4, Qupents: n=5, etc.
        :param n: Number to check for power of n shape.
        """

        def _is_power_of_n(x, n):
            if x < 1:
                return False
            while x % n == 0:
                x //= n
            return x == 1

        rows, cols = self.shape
        return _is_power_of_n(rows, n) and _is_power_of_n(cols, n)

    def is_hermitian(self) -> bool:
        """Check if the operator is Hermitian: U = U^dagger"""
        return np.allclose(self, self.conjugate_transpose())

    def is_identity(self) -> bool:
        """Check if the operator is the identity matrix."""
        return np.allclose(self, np.eye(self.shape[0]))

    def is_equal(self, other) -> bool:
        """Check if the operator is effectively equal to another operator."""
        return np.allclose(self, other, atol=1e-8)

    def num_levels(self) -> int:
        """Number of rows. Used for checking valid shapes."""
        return self.shape[0]

    def conjugate_transpose(self) -> np.ndarray:
        """
        Conjugate transpose (i.e. Hermitian adjoint or 'dagger operation') of the operator.
        1. Transpose the matrix
        2. Take the complex conjugate of each element (Flip the sign of the imaginary part)
        """
        return self.T.conj()

    def eigenvalues(self) -> np.ndarray:
        """
        Eigenvalues of the operator.
        Hermitian operators use eigvalsh for stable and faster computation.
        """
        return np.linalg.eigvalsh(self) if self.is_hermitian() else np.linalg.eigvals(self)

    def eigenvectors(self) -> np.ndarray:
        """
        Eigenvectors of the operator.
        Hermitian operators use eigh for stable and faster computation.
        """
        return np.linalg.eigh(self)[1] if self.is_hermitian() else np.linalg.eig(self)[1]

    def frobenius_norm(self) -> float:
        """Compute the Frobenius norm"""
        return np.linalg.norm(self)

    def commute(self, other: "Operator") -> bool:
        """
        Check if operator commute. U and V commute if UV = VU.
        :param other: Operator to check commutation with.
        """
        assert isinstance(other, Operator), "Other object must be a valid Operator."
        assert self.num_levels() == other.num_levels(), "Operators must have the same number of rows for the commutation check."
        return np.allclose(self @ other, other @ self)

    def to_qiskit(self) -> qiskit.quantum_info.Operator:
        """Convert operator to a Qiskit."""
        raise NotImplementedError(f"Conversion to Qiskit Gate is not implemented for {self.__class__.__name__}.")

    def from_qiskit(self, qiskit_operator: qiskit.quantum_info.Operator) -> "Operator":
        """
        Convert a Qiskit operator to scikit-q Operator.
        :param qiskit_operator: Qiskit Operator
        :return: scikit-q Operator object
        """
        raise NotImplementedError(f"Conversion from Qiskit is not implemented for {self.__class__.__name__}.")

    def to_pennylane(self):
        """Convert gate to a PennyLane gate object."""
        raise NotImplementedError(f"Conversion to PennyLane is not implemented for {self.__class__.__name__}.")

    def from_pennylane(self, pennylane_operator: qml.operation.Operation) -> "Operator":
        """
        Convert a PennyLane Operation to scikit-q Operator.
        :param pennylane_gate: PennyLane Operation object.
        :return: scikit-q Operator
        """
        raise NotImplementedError(f"Conversion from PennyLane is not implemented for {self.__class__.__name__}.")

    def __call__(self, other: np.ndarray) -> np.ndarray:
        """Call the operator on a quantum state."""
        return self.encodes(other)


class HermitianOperator(Operator):
    """
    Hermitian operator (observable) class.
    :param input_array: Input array to create the operator. Will be converted to a NumPy array.
    """

    def __new__(cls, input_array):
        obj = super().__new__(cls, input_array)
        assert obj.is_hermitian(), "Hermitian operator must be Hermitian."
        assert obj.is_at_least_nxn(n=2), "Hermitian operator must be at least a 2x2 matrix."
        return obj
