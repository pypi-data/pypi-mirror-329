import qiskit
import numpy as np
import scipy.linalg
import pennylane as qml

from ..base import HermitianOperator
from ..gates.qubit import X, Z, I


class Hamiltonian(HermitianOperator):
    """
    Class representing a Hamiltonian in quantum computing.

    :param input_array: The input array representing the Hamiltonian. Will be converted to a complex numpy array.
    :param hbar: The reduced Planck constant. Default is 1.0 (natural units).
    If you want to use the actual physical value, set hbar to 1.0545718e-34.
    """

    def __new__(cls, input_array, hbar: float = 1.0):
        assert hbar > 0, "The reduced Planck constant must be greater than zero."
        obj = super().__new__(cls, input_array)
        obj.hbar = hbar
        return obj

    @property
    def num_qubits(self) -> int:
        """Number of qubits in the Hamiltonian."""
        return int(np.log2(self.shape[0]))

    def is_multi_qubit(self) -> bool:
        """Check if Hamiltonian involves multiple qubits."""
        return self.num_qubits > 1

    def time_evolution_operator(self, t: float) -> np.ndarray:
        """Time evolution operator U(t) = exp(-iHt/hbar)."""
        return scipy.linalg.expm(-1j * self * t / self.hbar)

    def ground_state_energy(self) -> float:
        """Ground state energy. i.e. the smallest eigenvalue."""
        eigenvalues = self.eigenvalues()
        return eigenvalues[0]

    def ground_state(self) -> np.ndarray:
        """The eigenvector corresponding to the smallest eigenvalue."""
        _, eigenvectors = np.linalg.eigh(self)
        return eigenvectors[:, 0]

    def convert_endianness(self) -> "Hamiltonian":
        """Hamiltonian from big-endian to little-endian and vice versa."""
        perm = np.argsort([int(bin(i)[2:].zfill(self.num_qubits)[::-1], 2) for i in range(2**self.num_qubits)])
        return self[np.ix_(perm, perm)]

    def add_noise(self, noise_strength: float, noise_operator: np.array) -> "Hamiltonian":
        """
        Add noise to the Hamiltonian.
        :param noise_strength: Strength of the noise. Generally in range [0.0001, 0.5].
        :param noise_operator: Operator representing the noise. For example Pauli matrices.
        :return: A new Hamiltonian with noise added.
        """
        assert noise_operator.shape == self.shape, "Noise operator must have the same dimensions as the Hamiltonian."
        return Hamiltonian(self + noise_strength * noise_operator, hbar=self.hbar)

    def to_qiskit(self) -> qiskit.quantum_info.Operator:
        """
        Convert the scikit-q Hamiltonian to a Qiskit Operator object.
        Qiskit using little endian convention, so we permute the order of the qubits.
        :return: Qiskit Operator object
        """
        return qiskit.quantum_info.Operator(self.convert_endianness())

    @staticmethod
    def from_qiskit(operator: qiskit.quantum_info.Operator) -> "Hamiltonian":
        """
        Create a scikit-q Hamiltonian object from a Qiskit Operator object.
        Qiskit using little endian convention, so we permute the order of the qubits.
        :param operator: Qiskit Operator object
        :return: Hamiltonian object
        """
        return Hamiltonian(operator.data).convert_endianness()

    def to_pennylane(self, wires: list[int] | int = None, **kwargs) -> "qml.Hamiltonian":
        """
        Convert the scikit-q Hamiltonian to a PennyLane Hamiltonian.
        :param wires: List of wires to apply the Hamiltonian to
        kwargs are passed to the PennyLane Hamiltonian constructor.
        :return: PennyLane Hamiltonian object
        """
        coefficients = [1.0]
        wires = wires if wires is not None else list(range(self.num_qubits))
        observables = [qml.Hermitian(self, wires=wires)]
        return qml.Hamiltonian(coefficients, observables, **kwargs)

    @staticmethod
    def from_pennylane(hamiltonian: qml.Hamiltonian) -> "Hamiltonian":
        """
        Convert a PennyLane Hamiltonian object to a scikit-q Hamiltonian object.
        :param hamiltonian: PennyLane Hamiltonian object
        :return: Hamiltonian object
        """
        assert len(hamiltonian.ops) == 1, "Only single-term Hamiltonians are supported."
        return Hamiltonian(hamiltonian.ops[0].matrix())


class IsingHamiltonian(Hamiltonian):
    """
    Hamiltonian for the Ising model.
    :param num_qubits: Number of qubits in the system.
    :param J: Interaction strength between qubits.
    :param h: Transverse field strength.
    :param hbar: The reduced Planck constant. Default is 1.0 (natural units).
    """

    def __new__(cls, num_qubits: int, J: float, h: float, hbar: float = 1.0):
        size = 2**num_qubits
        H = np.zeros((size, size), dtype=complex)
        # Interaction term: -J * sum(Z_i Z_{i+1})
        for i in range(num_qubits - 1):
            term = np.eye(1)
            for j in range(num_qubits):
                if j == i or j == i + 1:
                    term = np.kron(term, Z())
                else:
                    term = np.kron(term, I())
            H -= J * term

        # Transverse field term: -h * sum(X_i)
        for i in range(num_qubits):
            term = np.eye(1)
            for j in range(num_qubits):
                if j == i:
                    term = np.kron(term, X())
                else:
                    term = np.kron(term, I())
            H -= h * term

        return super().__new__(cls, H, hbar)


class HeisenbergHamiltonian(Hamiltonian):
    """
    Hamiltonian for the Heisenberg model.
    :param num_qubits: Number of qubits in the system.
    :param J: Interaction strength between qubits.
    :param hbar: The reduced Planck constant. Default is 1.0 (natural units).
    """

    def __new__(cls, num_qubits: int, J: float, hbar: float = 1.0):
        size = 2**num_qubits
        H = np.zeros((size, size), dtype=complex)

        # Interaction term: J * sum(X_i X_{i+1} + Y_i Y_{i+1} + Z_i Z_{i+1})
        for i in range(num_qubits - 1):
            X_i = np.array([[0, 1], [1, 0]])
            Y_i = np.array([[0, -1j], [1j, 0]])
            Z_i = np.array([[1, 0], [0, -1]])
            H += J * (np.kron(np.kron(np.eye(2**i), np.kron(X_i, X_i)), np.eye(2 ** (num_qubits - i - 2))) + np.kron(np.kron(np.eye(2**i), np.kron(Y_i, Y_i)), np.eye(2 ** (num_qubits - i - 2))) + np.kron(np.kron(np.eye(2**i), np.kron(Z_i, Z_i)), np.eye(2 ** (num_qubits - i - 2))))

        return super().__new__(cls, H, hbar)
