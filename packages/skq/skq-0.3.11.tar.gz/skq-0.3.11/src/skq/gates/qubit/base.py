import qiskit
import numpy as np
import scipy as sp
import pennylane as qml
from qiskit import QuantumCircuit

from ..base import BaseGate


# I, X, Y, Z Pauli matrices
SINGLE_QUBIT_PAULI_MATRICES = [
    np.eye(2, dtype=complex),  # I
    np.array([[0, 1], [1, 0]], dtype=complex),  # X
    np.array([[0, -1j], [1j, 0]], dtype=complex),  # Y
    np.array([[1, 0], [0, -1]], dtype=complex),  # Z
]
# Any two-qubit Pauli matrix can be expressed as a Kronecker product of two single-qubit Pauli matrices
TWO_QUBIT_PAULI_MATRICES = [np.kron(pauli1, pauli2) for pauli1 in SINGLE_QUBIT_PAULI_MATRICES for pauli2 in SINGLE_QUBIT_PAULI_MATRICES]

# X, Y, Z, H and S gates are Clifford gates
SINGLE_QUBIT_CLIFFORD_MATRICES = SINGLE_QUBIT_PAULI_MATRICES + [
    np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),  # H
    np.array([[1, 0], [0, 1j]], dtype=complex),  # S
]
# Two qubit Clifford gates can be expressed as a Kronecker product of two single-qubit Clifford gates + CNOT and SWAP
TWO_QUBIT_CLIFFORD_MATRICES = [np.kron(clifford1, clifford2) for clifford1 in SINGLE_QUBIT_CLIFFORD_MATRICES for clifford2 in SINGLE_QUBIT_CLIFFORD_MATRICES] + [
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex),  # CX (CNOT)
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]], dtype=complex),  # CY
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=complex),  # CZ
    np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex),  # SWAP
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1 / np.sqrt(2), 1 / np.sqrt(2)], [0, 0, 1 / np.sqrt(2), -1 / np.sqrt(2)]], dtype=complex),  # CH
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]], dtype=complex),  # CS
]


class QubitGate(BaseGate):
    """
    Base class for Qubit gates.
    A quantum system with 2 basis states (|0>, |1>).
    Models spin-1/2 particles like electrons.
    """

    def __new__(cls, input_array):
        obj = super().__new__(cls, input_array)
        assert obj.is_at_least_nxn(n=2), "Gate must be at least a 2x2 matrix."
        assert obj.is_power_of_n_shape(n=2), "Gate shape must be a power of 2."
        return obj

    @property
    def num_qubits(self) -> int:
        """Return the number of qubits involved in the gate."""
        return int(np.log2(self.shape[0]))

    def is_multi_qubit(self) -> bool:
        """Check if the gate involves multiple qubits."""
        return self.num_qubits > 1

    def is_pauli(self) -> bool:
        """Check if the gate is a Pauli gate."""
        # I, X, Y, Z Pauli matrices
        if self.num_qubits == 1:
            return any(np.allclose(self, pauli) for pauli in SINGLE_QUBIT_PAULI_MATRICES)
        # Combinations of single-qubit Pauli matrices
        elif self.num_qubits == 2:
            return any(np.allclose(self, pauli) for pauli in TWO_QUBIT_PAULI_MATRICES)
        else:
            return NotImplementedError("Pauli check not supported for gates with more than 2 qubits")

    def is_clifford(self) -> bool:
        """Check if the gate is a Clifford gate."""
        # X, Y, Z, H and S
        if self.num_qubits == 1:
            return any(np.allclose(self, clifford) for clifford in SINGLE_QUBIT_CLIFFORD_MATRICES)
        # Combinations of single-qubit Clifford gates + CNOT and SWAP
        elif self.num_qubits == 2:
            return any(np.allclose(self, clifford) for clifford in TWO_QUBIT_CLIFFORD_MATRICES)
        else:
            return NotImplementedError("Clifford check not supported for gates with more than 2 qubits")

    def sqrt(self) -> "CustomQubitGate":
        """Compute the square root of the gate."""
        sqrt_matrix = sp.linalg.sqrtm(self)
        return CustomQubitGate(sqrt_matrix)

    def kron(self, other: "QubitGate") -> "CustomQubitGate":
        """Compute the Kronecker product of two gates."""
        kron_matrix = np.kron(self, other)
        return CustomQubitGate(kron_matrix)

    def convert_endianness(self) -> "QubitGate":
        """Convert a gate matrix from big-endian to little-endian and vice versa."""
        if self.num_qubits == 1:
            return self
        permutation = np.arange(2**self.num_qubits).reshape([2] * self.num_qubits).transpose().flatten()
        return self[permutation][:, permutation]

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        """
        Convert gate to a Qiskit Gate object.
        Qiskit using little endian convention, so we permute the order of the qubits.
        :return: Qiskit UnitaryGate object
        """
        gate_name = self.__class__.__name__
        print(f"No to_qiskit defined for '{gate_name}'. Initializing as UnitaryGate.")
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label=gate_name)

    @staticmethod
    def from_qiskit(gate: qiskit.circuit.gate.Gate) -> "CustomQubitGate":
        """
        Convert a Qiskit Gate to skq CustomGate.
        Qiskit using little endian convention, so we permute the order of the qubits.
        :param gate: Qiskit Gate object
        """
        assert isinstance(gate, qiskit.circuit.gate.Gate), "Input must be a Qiskit Gate object"
        return CustomQubitGate(gate.to_matrix()).convert_endianness()

    def to_pennylane(self, wires: list[int] | int = None) -> qml.QubitUnitary:
        """
        Convert gate to a PennyLane QubitUnitary.
        PennyLane use the big endian convention, so no need to reverse the order of the qubits.
        :param wires: List of wires the gate acts on
        :return: PennyLane QubitUnitary object
        """
        gate_name = self.__class__.__name__
        print(f"No to_pennylane defined for '{gate_name}'. Initializing as QubitUnitary.")
        wires = wires if wires is not None else list(range(self.num_qubits))
        return qml.QubitUnitary(self, wires=wires)

    @staticmethod
    def from_pennylane(gate: qml.operation.Operation) -> "CustomQubitGate":
        """
        Convert a PennyLane Operation to skqq CustomGate.
        PennyLane use the big endian convention, so no need to reverse the order of the qubits.
        :param gate: PennyLane Operation object
        """
        assert isinstance(gate, qml.operation.Operation), "Input must be a PennyLane Operation object"
        return CustomQubitGate(gate.matrix())

    def to_qasm(self, qubits: list[int]) -> str:
        """
        Convert gate to a OpenQASM string.
        More information on OpenQASM (2.0): https://arxiv.org/pdf/1707.03429
        OpenQASM specification: https://openqasm.com/intro.html
        Gates should be part of the standard library.
        OpenQASM 2.0 -> qelib1.inc
        OpenQASM 3 -> stdgates.inc
        :param qubits: List of qubit indices the gate acts on
        :return: OpenQASM string representation of the gate
        String representation should define gate, qubits it acts on and ;.
        Example for Hadamard in 1st qubit -> "h q[0];"
        """
        raise NotImplementedError("Conversion to OpenQASM is not implemented.")

    @staticmethod
    def from_qasm(qasm_string: str) -> "QubitGate":
        """Convert a OpenQASM string to scikit-q gate."""
        raise NotImplementedError("Conversion from OpenQASM is not implemented.")

    def draw(self, **kwargs):
        """Draw the gate using a Qiskit QuantumCircuit."""
        qc = QuantumCircuit(self.num_qubits)
        qc.append(self.to_qiskit(), range(self.num_qubits))
        return qc.draw(**kwargs)


class CustomQubitGate(QubitGate):
    """Bespoke Qubit gate."""

    def __new__(cls, input_array):
        obj = super().__new__(cls, input_array)
        return obj
