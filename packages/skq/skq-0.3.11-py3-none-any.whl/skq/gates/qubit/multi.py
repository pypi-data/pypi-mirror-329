import qiskit
import numpy as np
import pennylane as qml

from .base import QubitGate
from .single import X, Y, Z
from ...quantum_info.state import Statevector


class DeutschOracle(QubitGate):
    """
    Oracle for Deutsch algorithm with ancilla qubit.
    Implements |x,y⟩ -> |x, y⊕f(x)⟩

    :param f: Function that takes an integer x (0 or 1) and returns 0 or 1
    """

    def __new__(cls, f):
        matrix = np.zeros((4, 4))
        for x in [0, 1]:
            matrix[x * 2 + f(x), x * 2] = 1  # |x,0⟩ -> |x,f(x)⟩
            matrix[x * 2 + (1 - f(x)), x * 2 + 1] = 1  # |x,1⟩ -> |x,1-f(x)⟩

        return super().__new__(cls, matrix)


class DeutschJozsaOracle(QubitGate):
    """
    Oracle for Deutsch-Jozsa algorithm.

    For input x and output f(x), the oracle applies phase (-1)^f(x).
    - Constant function: f(x) is same for all x
    - Balanced function: f(x) = 1 for exactly half of inputs

    :param f: Function that takes an integer x (0 to 2^n-1) and returns 0 or 1
    :param n_bits: Number of input bits
    """

    def __new__(cls, f, n_bits: int):
        n_states = 2**n_bits
        outputs = [f(x) for x in range(n_states)]
        if not all(v in [0, 1] for v in outputs):
            raise ValueError("Function must return 0 or 1")

        ones = sum(outputs)
        if ones != 0 and ones != n_states and ones != n_states // 2:
            raise ValueError("Function must be constant or balanced")

        oracle_matrix = np.eye(n_states)
        for x in range(n_states):
            oracle_matrix[x, x] = (-1) ** f(x)

        return super().__new__(cls, oracle_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="DeutschJozsaOracle")


class PhaseOracle(QubitGate):
    """
    Phase Oracle as used in Grover's search algorithm.
    :param target_state: The target state to mark.
    target_state is assumed to be in Big-Endian format.
    """

    def __new__(cls, target_state: np.ndarray):
        state = Statevector(target_state)
        n_qubits = state.num_qubits
        identity = np.eye(2**n_qubits)
        oracle_matrix = identity - 2 * np.outer(target_state, target_state.conj())
        return super().__new__(cls, oracle_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="PhaseOracle")


class GroverDiffusion(QubitGate):
    """
    Grover Diffusion Operator Gate as used in Grover's search algorithm.
    This gate amplifies the amplitude of the marked state.
    :param n_qubits: The number of qubits in the system.
    """

    def __new__(cls, n_qubits: int):
        assert n_qubits >= 1, "GroverDiffusionGate must have at least one qubit."
        # Equal superposition state vector
        size = 2**n_qubits
        equal_superposition = np.ones(size) / np.sqrt(size)
        # Grover diffusion operator: 2|ψ⟩⟨ψ| - I
        diffusion_matrix = 2 * np.outer(equal_superposition, equal_superposition) - np.eye(size)
        return super().__new__(cls, diffusion_matrix)

    def to_qiskit(self) -> qiskit.circuit.library.UnitaryGate:
        # Reverse the order of qubits for Qiskit's little-endian convention
        return qiskit.circuit.library.UnitaryGate(self.convert_endianness(), label="GroverDiffusion")


class CX(QubitGate):
    """
    Controlled-X (CNOT) gate.
    Used to entangle two qubits.
    If the control qubit is |1>, the target qubit is flipped.
    """

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CXGate:
        return qiskit.circuit.library.CXGate()

    def to_pennylane(self, wires: list[int]) -> qml.CNOT:
        assert len(wires) == 2, "PennyLane CX gate requires 2 wires."
        return qml.CNOT(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CX gate requires 2 qubits."
        return f"cx q[{qubits[0]}], q[{qubits[1]}];"


class CY(QubitGate):
    """Controlled-Y gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CYGate:
        return qiskit.circuit.library.CYGate()

    def to_pennylane(self, wires: list[int]) -> qml.CY:
        assert len(wires) == 2, "PennyLane CY gate requires 2 wires."
        return qml.CY(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CY gate requires 2 qubits."
        return f"cy q[{qubits[0]}], q[{qubits[1]}];"


class CZ(QubitGate):
    """Controlled-Z gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

    def to_qiskit(self) -> qiskit.circuit.library.CZGate:
        return qiskit.circuit.library.CZGate()

    def to_pennylane(self, wires: list[int]) -> qml.CZ:
        assert len(wires) == 2, "PennyLane CZ gate requires 2 wires."
        return qml.CZ(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CZ gate requires 2 qubits."
        return f"cz q[{qubits[0]}], q[{qubits[1]}];"


class CH(QubitGate):
    """Controlled-Hadamard gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1 / np.sqrt(2), 1 / np.sqrt(2)], [0, 0, 1 / np.sqrt(2), -1 / np.sqrt(2)]])

    def to_qiskit(self) -> qiskit.circuit.library.CHGate:
        return qiskit.circuit.library.CHGate()

    def to_pennylane(self, wires: list[int]) -> qml.CH:
        assert len(wires) == 2, "PennyLane CH gate requires 2 wires."
        return qml.CH(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CH gate requires 2 qubits."
        return f"ch q[{qubits[0]}], q[{qubits[1]}];"


class CPhase(QubitGate):
    """General controlled phase shift gate.
    :param phi: The phase shift angle in radians.
    """

    def __new__(cls, phi: float):
        obj = super().__new__(cls, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j * phi)]])
        obj.phi = phi
        return obj

    def to_qiskit(self) -> qiskit.circuit.library.CPhaseGate:
        return qiskit.circuit.library.CPhaseGate(self.phi)

    def to_pennylane(self, wires: list[int]) -> qml.CPhase:
        assert len(wires) == 2, "PennyLane CPhase gate requires 2 wires."
        return qml.CPhase(phi=self.phi, wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM CPhase gate requires 2 qubits."
        return f"cp({self.phi}) q[{qubits[0]}], q[{qubits[1]}];"


class CS(CPhase):
    """Controlled-S gate."""

    def __new__(cls):
        phi = np.pi / 2
        return super().__new__(cls, phi=phi)

    def to_qiskit(self) -> qiskit.circuit.library.CSGate:
        return qiskit.circuit.library.CSGate()


class CT(CPhase):
    """Controlled-T gate."""

    def __new__(cls):
        phi = np.pi / 4
        return super().__new__(cls, phi=phi)

    def to_qiskit(self) -> qiskit.circuit.library.TGate:
        return qiskit.circuit.library.TGate().control(1)


class SWAP(QubitGate):
    """Swap gate. Swaps the states of two qubits."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    def to_qiskit(self) -> qiskit.circuit.library.SwapGate:
        return qiskit.circuit.library.SwapGate()

    def to_pennylane(self, wires: list[int]) -> qml.SWAP:
        assert len(wires) == 2, "PennyLane SWAP gate requires 2 wires."
        return qml.SWAP(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 2, "OpenQASM SWAP gate requires 2 qubits."
        return f"swap q[{qubits[0]}], q[{qubits[1]}];"


class CSwap(QubitGate):
    """A controlled-SWAP gate. Also known as the Fredkin gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1]])

    def to_qiskit(self) -> qiskit.circuit.library.CSwapGate:
        return qiskit.circuit.library.CSwapGate()

    def to_pennylane(self, wires: list[int]) -> qml.CSWAP:
        return qml.CSWAP(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CSWAP gate requires 3 qubits."
        return f"cswap q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];"


class CCX(QubitGate):
    """A 3-qubit controlled-controlled-X (CCX) gate. Also known as the Toffoli gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.CCXGate:
        return qiskit.circuit.library.CCXGate()

    def to_pennylane(self, wires: list[int]) -> qml.Toffoli:
        return qml.Toffoli(wires=wires)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCX (Toffoli) gate requires 3 qubits."
        return f"ccx q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];"


class CCY(QubitGate):
    """A 3-qubit controlled-controlled-Y (CCY) gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1j], [0, 0, 0, 0, 0, 0, 1j, 0]])

    def to_qiskit(self) -> qiskit.circuit.library.YGate:
        # There is no native CCY gate in Qiskit so we construct it.
        return qiskit.circuit.library.YGate().control(2)

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCY gate requires 3 qubits."
        # Custom OpenQASM implementation
        # sdg is an inverse s gate
        return f"""sdg q[{qubits[2]}];\ncx q[{qubits[1]}], q[{qubits[2]}];\ns q[{qubits[2]}];\ncx q[{qubits[0]}], q[{qubits[2]}];\nsdg q[{qubits[2]}];\ncx q[{qubits[1]}], q[{qubits[2]}];\ns q[{qubits[2]}];\ny q[{qubits[2]}];"""


class CCZ(QubitGate):
    """A 3-qubit controlled-controlled-Z (CCZ) gate."""

    def __new__(cls):
        return super().__new__(cls, [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, -1]])

    def to_qiskit(self) -> qiskit.circuit.library.CCZGate:
        return qiskit.circuit.library.CCZGate()

    def to_qasm(self, qubits: list[int]) -> str:
        assert len(qubits) == 3, "OpenQASM CCZ gate requires 3 qubits."
        # CCZ = CCX sandwiched between two H gates on last qubit.
        return f"""h q[{qubits[2]}];\nccx q[{qubits[0]}], q[{qubits[1]}], q[{qubits[2]}];\nh q[{qubits[2]}];"""


class MCX(QubitGate):
    """
    Multi controlled-X (MCX) gate.
    :param num_ctrl_qubits: Number of control qubits.
    """

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCX gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = X()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.CXGate | qiskit.circuit.library.CCXGate | qiskit.circuit.library.C3XGate | qiskit.circuit.library.C4XGate | qiskit.circuit.library.MCXGate:
        if self.num_ctrl_qubits == 1:
            return qiskit.circuit.library.CXGate()
        elif self.num_ctrl_qubits == 2:
            return qiskit.circuit.library.CCXGate()
        elif self.num_ctrl_qubits == 3:
            return qiskit.circuit.library.C3XGate()
        elif self.num_ctrl_qubits == 4:
            return qiskit.circuit.library.C4XGate()
        else:
            return qiskit.circuit.library.MCXGate(num_ctrl_qubits=self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CNOT | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CNOT(wires=wires)
        else:
            return super().to_pennylane(wires)


class MCY(QubitGate):
    """Multi controlled-Y (MCY) gate."""

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCY gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = Y()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.YGate:
        return qiskit.circuit.library.YGate().control(self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CY | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CY(wires=wires)
        else:
            return super().to_pennylane(wires)


class MCZ(QubitGate):
    """Multi controlled-Z (MCZ) gate."""

    def __new__(cls, num_ctrl_qubits: int):
        assert num_ctrl_qubits >= 1, "MCZ gate must have at least one control qubit."
        cls.num_ctrl_qubits = num_ctrl_qubits
        levels = 2 ** (num_ctrl_qubits + 1)
        gate = np.identity(levels)
        gate[-2:, -2:] = Z()
        return super().__new__(cls, gate)

    def to_qiskit(self) -> qiskit.circuit.library.ZGate:
        return qiskit.circuit.library.ZGate().control(self.num_ctrl_qubits)

    def to_pennylane(self, wires: list[int]) -> qml.CZ | qml.QubitUnitary:
        if self.num_ctrl_qubits == 1:
            return qml.CZ(wires=wires)
        else:
            return super().to_pennylane(wires)


class CR(QubitGate):
    """Simple Cross-Resonance gate."""

    def __new__(cls, theta: float):
        return super().__new__(cls, [[1, 0, 0, 0], [0, np.cos(theta), 0, -1j * np.sin(theta)], [0, 0, 1, 0], [0, -1j * np.sin(theta), 0, np.cos(theta)]])


class SymmetricECR(QubitGate):
    """Symmetric Echoed Cross-Resonance gate."""

    def __new__(cls, theta: float):
        return super().__new__(cls, CR(theta) @ CR(-theta))


class AsymmetricECR(QubitGate):
    """Asymmetric Echoed Cross-Resonance gate."""

    def __new__(cls, theta1: float, theta2: float):
        return super().__new__(cls, CR(theta1) @ CR(theta2))
