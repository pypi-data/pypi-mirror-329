import qiskit
import numpy as np
import pennylane as qml
from scipy.linalg import expm

from ..base import HermitianOperator
from ..constants import BOLTZMANN_CONSTANT
from ..gates.qubit import X, Y, Z


class DensityMatrix(HermitianOperator):
    """Density matrix representation of a qubit state."""

    def __new__(cls, input_array):
        obj = super().__new__(cls, input_array)
        assert obj.is_positive_semidefinite(), "Density matrix must be positive semidefinite (All eigenvalues >= 0)."
        assert obj.trace_equal_to_one(), "Density matrix must have trace equal to one. Normalize to unit trace if you want to use this matrix as a DensityMatrix."
        return obj

    @property
    def num_qubits(self) -> int:
        """Number of qubits in the density matrix."""
        return int(np.log2(len(self)))

    def is_positive_semidefinite(self):
        """Matrix is positive semidefinite."""
        eigenvalues = np.linalg.eigvalsh(self)
        return np.all(eigenvalues >= 0)

    def is_pure(self) -> bool:
        """Check if density matrix is pure."""
        return np.isclose(np.trace(self @ self), 1)

    def is_mixed(self) -> bool:
        """Check if density matrix is mixed."""
        return not self.is_pure()

    def trace_equal_to_one(self) -> bool:
        """Trace of density matrix is equal to one."""
        return np.isclose(np.trace(self), 1)

    def probabilities(self) -> float:
        """Probabilities of all possible state measurements."""
        return np.diag(self).real

    def is_multi_qubit(self) -> bool:
        """Check if the density matrix represents a multi-qubit state."""
        return self.num_qubits > 1

    def trace_norm(self) -> float:
        """Trace norm of the density matrix."""
        return np.trace(np.sqrt(self.conjugate_transpose() @ self))

    def distance(self, other: "DensityMatrix") -> float:
        """Trace norm distance between two density matrices."""
        assert isinstance(other, DensityMatrix), "'other' argument must be a valid DensityMatrix object."
        return self.trace_norm(self - other)

    def bloch_vector(self) -> np.ndarray:
        """Bloch vector of the density matrix."""
        if self.num_qubits > 1:
            raise NotImplementedError("Bloch vector is not yet implemented for multi-qubit states.")

        # Bloch vector components
        bx = np.trace(np.dot(self, X())).real
        by = np.trace(np.dot(self, Y())).real
        bz = np.trace(np.dot(self, Z())).real
        return np.array([bx, by, bz])

    def kron(self, other: "DensityMatrix") -> "DensityMatrix":
        """
        Kronecker (tensor) product of two density matrices.
        This can be used to create so-called "product states" that represent
        the independence between two quantum systems.
        :param other: DensityMatrix object
        :return: Kronecker product of the two density matrices
        """
        return DensityMatrix(np.kron(self, other))

    def entropy(self):
        """von Neumann entropy."""
        eigenvals = self.eigenvalues()
        # Only consider non-zero eigenvalues
        nonzero_eigenvalues = eigenvals[eigenvals > 0]
        return -np.sum(nonzero_eigenvalues * np.log(nonzero_eigenvalues))

    def internal_energy(self, hamiltonian: np.array) -> float:
        """
        Expected value of the Hamiltonian.
        :param hamiltonian: Hamiltonian matrix
        :return: Expected value of the Hamiltonian
        """
        return np.trace(self @ hamiltonian)

    def to_qiskit(self) -> qiskit.quantum_info.DensityMatrix:
        """
        Convert the density matrix to a Qiskit DensityMatrix object.
        :return: Qiskit DensityMatrix object
        """
        return qiskit.quantum_info.DensityMatrix(self)

    @staticmethod
    def from_qiskit(density_matrix: qiskit.quantum_info.DensityMatrix) -> "DensityMatrix":
        """
        Create a DensityMatrix object from a Qiskit DensityMatrix object.
        :param density_matrix: Qiskit DensityMatrix object
        :return: DensityMatrix object
        """
        return DensityMatrix(density_matrix.data)

    def to_pennylane(self, wires: list[int] | int = None) -> qml.QubitDensityMatrix:
        """
        Convert the density matrix to a PennyLane QubitDensityMatrix.
        :param wires: List of wires to apply the density matrix to
        :return: PennyLane QubitDensityMatrix object
        """
        wires = wires if wires is not None else range(self.num_qubits)
        return qml.QubitDensityMatrix(self, wires=wires)

    @staticmethod
    def from_pennylane(density_matrix: qml.QubitDensityMatrix) -> "DensityMatrix":
        """
        Convert a PennyLane QubitDensityMarix object to a scikit-q StateVector.
        :param density_matrix: PennyLane QubitDensityMatrix object
        :return: scikit-q StateVector object
        """
        return DensityMatrix(density_matrix.data[0])

    @staticmethod
    def from_probabilities(probabilities: np.array) -> "DensityMatrix":
        """
        Create a density matrix from a list of probabilities.
        :param probabilities: A 1D array of probabilities
        :return: Density matrix
        """
        assert np.isclose(np.sum(probabilities), 1), f"Probabilities must sum to one. Got sum: {np.sum(probabilities)}"
        assert len(probabilities.shape) == 1, f"Probabilities must be a 1D array. Got shape: {probabilities.shape}"
        return DensityMatrix(np.diag(probabilities))


class GibbsState(DensityMatrix):
    """
    Gibbs (mixed) state representation of a quantum state in thermal equilibrium.
    :param hamiltonian: Hamiltonian matrix of the system
    :param temperature: Temperature of the system in Kelvin
    """

    def __new__(cls, hamiltonian: np.array, temperature: float):
        cls.hamiltonian = hamiltonian
        cls.temperature = temperature
        cls.beta = 1 / (BOLTZMANN_CONSTANT * temperature)
        cls.exp_neg_beta_H = expm(-cls.beta * hamiltonian)
        cls.partition_function = np.trace(cls.exp_neg_beta_H)
        density_matrix = cls.exp_neg_beta_H / cls.partition_function
        return super().__new__(cls, density_matrix)

    def free_energy(self) -> float:
        """Helmholtz free energy."""
        return -BOLTZMANN_CONSTANT * self.temperature * np.log(self.partition_function)

    def heat_capacity(self) -> float:
        """Calculate the heat capacity."""
        beta = 1 / (BOLTZMANN_CONSTANT * self.temperature)
        energy_squared = np.trace(self @ self.hamiltonian @ self.hamiltonian)
        energy_mean = self.internal_energy(self.hamiltonian) ** 2
        return beta**2 * (energy_squared - energy_mean)
