import qiskit
import numpy as np
from scipy.linalg import svd

from ..quantum_info.density import DensityMatrix


class Statevector(np.ndarray):
    """
    Statevector representation for a quantum (qubit) state.
    NOTE: Input is assumed to be in big-endian format.
    Little-endian -> Least significant qubit (LSB) is on the right. Like |q1 q0> where q0 is the LSB.
    Big-endian -> Least significant qubit (LSB) is on the left. Like |q0 q1> where q0 is the LSB.
    """

    def __new__(cls, input_array):
        arr = np.asarray(input_array, dtype=complex)
        obj = arr.view(cls)
        assert obj.is_1d(), "State vector must be 1D."
        assert obj.is_normalized(), "State vector must be normalized."
        assert obj.is_power_of_two_len(), "State vector length must be a least length 2 and a power of 2."
        return obj

    @property
    def num_qubits(self) -> int:
        """Number of qubits in the state vector."""
        return int(np.log2(len(self)))

    def is_1d(self) -> bool:
        """State vector is 1D."""
        return self.ndim == 1

    def is_normalized(self) -> bool:
        """State vector is normalized: ||ψ|| = 1."""
        return np.isclose(np.linalg.norm(self), 1)

    def is_power_of_two_len(self) -> bool:
        """Check if a number is a power of two"""
        n = len(self)
        return n >= 2 and (n & (n - 1)) == 0

    def is_multi_qubit(self) -> bool:
        """State vector represents a multi-qubit state."""
        return self.num_qubits > 1

    def is_indistinguishable(self, other: "Statevector") -> bool:
        """Two state vectors are indistinguishable if their density matrices are the same."""
        return np.allclose(self.density_matrix(), other.density_matrix())

    def magnitude(self) -> float:
        """Magnitude (or norm) of the state vector. sqrt(<ψ|ψ>)"""
        np.linalg.norm(self)

    def expectation(self, operator: np.array) -> float:
        """
        Expectation value of an observable with respect to the quantum state.
        computes <ψ|O|ψ>
        :param operator: The observable (Hermitian matrix) as a 2D numpy array.
        :return: Expectation value.
        """
        assert len(operator.shape) == 2, "The operator must be a 2D matrix."
        assert np.allclose(operator, operator.T.conj()), "The operator must be Hermitian."
        return float(np.real(self.conjugate_transpose() @ operator @ self))

    def density_matrix(self) -> DensityMatrix:
        """Return the density matrix representation of the state vector."""
        return DensityMatrix(np.outer(self, self.conj()))

    def probabilities(self) -> np.ndarray:
        """Probabilities of all possible states."""
        return np.abs(self) ** 2

    def measure_index(self) -> int:
        """
        Simulate a measurement of the state and get a sampled index.
        :return: Index of the measured state.
        For example:
        |0> -> 0
        |00> -> 0
        |11> -> 3
        """
        return np.random.choice(len(self), p=self.probabilities())

    def measure_bitstring(self) -> str:
        """
        Simulate a measurement of the state vector and get a bitstring representing the sample.
        :return: Bitstring representation of the measured state.
        For example:
        |0> -> "0"
        |00> -> "00"
        |11> -> "11"
        """
        return bin(self.measure_index())[2:].zfill(self.num_qubits)

    def reverse(self) -> "Statevector":
        """Reverse the order of the state vector to account for endianness.
        For example Qiskit uses little endian convention.
        Little-endian -> Least significant qubit (LSB) is on the right. Like |q1 q0> where q0 is the LSB.
        Big-endian -> Least significant qubit (LSB) is on the left. Like |q0 q1> where q0 is the LSB.
        """
        return Statevector(self[::-1])

    def bloch_vector(self) -> np.ndarray:
        """Bloch vector representation of the quantum state."""
        return self.density_matrix().bloch_vector()

    def conjugate_transpose(self) -> np.ndarray:
        """Conjugate transpose (Hermitian adjoint) of the state vector."""
        return self.T.conj()

    def orthonormal_basis(self) -> np.ndarray:
        """
        Orthonormal basis using the Gram-Schmidt process.
        :return: 2D array representing the orthonormal basis.
        """
        return np.array([self / np.linalg.norm(self)]).T

    def schmidt_decomposition(self) -> tuple[np.array, np.array, np.array]:
        """
        Perform Schmidt decomposition on a quantum state.
        :return: Tuple of Schmidt coefficients, Basis A and Basis B
        """
        # Infer dimensions
        N = len(self)
        dim_A = int(np.sqrt(N))
        dim_B = N // dim_A

        # Singular Value Decomposition
        state_matrix = self.reshape(dim_A, dim_B)
        U, S, Vh = svd(state_matrix)

        # Coefficients (S), Basis A (U) and Basis B (Vh^dagger)
        return S, U, Vh.conj().T

    def to_qiskit(self) -> qiskit.quantum_info.Statevector:
        """
        Convert the state vector to a Qiskit QuantumCircuit object.
        Qiskit uses little-endian convention.
        :return: Qiskit StateVector object
        """
        return qiskit.quantum_info.Statevector(self.reverse())

    @staticmethod
    def from_qiskit(statevector: qiskit.quantum_info.Statevector) -> "Statevector":
        """
        Convert a Qiskit StateVector object to a scikit-q StateVector.
        Qiskit uses little-endian convention.
        :param statevector: Qiskit StateVector object
        :return: scikit-q StateVector object
        """
        return Statevector(statevector.data).reverse()

    def to_pyquil(self):
        """
        Convert the state vector to a PyQuil object.
        PyQuil uses little-endian convention.
        :return: PyQuil object
        """
        raise NotImplementedError("Conversion to PyQuil is not implemented.")

    @staticmethod
    def from_pyquil(statevector) -> "Statevector":
        """
        Convert a PyQuil object to a scikit-q StateVector object.
        PyQuil uses little-endian convention.
        :return: scikit-q StateVector object
        """
        raise NotImplementedError("Conversion from PyQuil is not implemented.")


class ZeroState(Statevector):
    """Zero state |0...0>"""

    def __new__(cls, num_qubits: int):
        return super().__new__(cls, [1] + [0] * (2**num_qubits - 1))


class OneState(Statevector):
    """One state |1...1>"""

    def __new__(cls, num_qubits: int):
        return super().__new__(cls, [0] * (2**num_qubits - 1) + [1])


class PlusState(Statevector):
    """Single Qubit |+> superposition state"""

    def __new__(cls):
        return super().__new__(cls, [1, 1] / np.sqrt(2))


class MinusState(Statevector):
    """Single Qubit |-> superposition state"""

    def __new__(cls):
        return super().__new__(cls, [1, -1] / np.sqrt(2))


class PhiPlusState(Statevector):
    """Bell state |Φ+>"""

    def __new__(cls):
        return super().__new__(cls, [1, 0, 0, 1] / np.sqrt(2))


class PhiMinusState(Statevector):
    """Bell state |Φ->"""

    def __new__(cls):
        return super().__new__(cls, [1, 0, 0, -1] / np.sqrt(2))


class PsiPlusState(Statevector):
    """Bell state |Ψ+>"""

    def __new__(cls):
        return super().__new__(cls, [0, 1, 1, 0] / np.sqrt(2))


class PsiMinusState(Statevector):
    """Bell state |Ψ->"""

    def __new__(cls):
        return super().__new__(cls, [0, 1, -1, 0] / np.sqrt(2))


class GHZState(Statevector):
    """GHZ state |0...0> + |1...1>"""

    def __new__(cls, num_qubits: int):
        assert num_qubits >= 3, "GHZ state requires at least 3 qubits."
        state = np.zeros(2**num_qubits)
        state[0] = 1 / np.sqrt(2)
        state[-1] = 1 / np.sqrt(2)
        return super().__new__(cls, state)


class WState(Statevector):
    """W state |001> + |010> + |100>"""

    def __new__(cls, num_qubits: int):
        assert num_qubits >= 3, "W state requires at least 3 qubits."
        state = np.zeros(2**num_qubits)
        for i in range(num_qubits):
            state[2**i] = 1 / np.sqrt(num_qubits)
        return super().__new__(cls, state)
