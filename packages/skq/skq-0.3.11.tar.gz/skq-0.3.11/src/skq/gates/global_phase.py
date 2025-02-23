import qiskit
import numpy as np
import pennylane as qml

from .base import BaseGate


class GlobalPhase(BaseGate):
    """
    Class representing a Global Phase
    :param phase: Global phase angle in radians
    """

    def __new__(cls, phase: float) -> "GlobalPhase":
        input_array = np.array([[np.exp(1j * phase)]], dtype=complex)
        obj = super().__new__(cls, input_array)
        assert obj.is_1x1(), "Quscalar must be a 1x1 matrix"
        return obj

    @property
    def scalar(self) -> complex:
        """Get the scalar value of the gate."""
        return self[0, 0]

    @property
    def phase(self) -> float:
        """Get the global phase."""
        return np.angle(self.scalar)

    def is_1x1(self) -> bool:
        """Check if the gate is a 1x1 matrix."""
        return self.shape == (1, 1)

    def inverse(self) -> "GlobalPhase":
        inverse_phase = -self.phase
        return GlobalPhase(inverse_phase)

    def combine(self, other: "GlobalPhase") -> "GlobalPhase":
        assert isinstance(other, GlobalPhase), "Can only combine with another QuScalarGate."
        combined_phase = self.phase + other.phase
        return GlobalPhase(combined_phase)

    def multiply(self, other: "GlobalPhase") -> "GlobalPhase":
        assert isinstance(other, GlobalPhase), "Can only multiply with another QuScalarGate."
        multiplied_phase = np.angle(self.scalar * other.scalar)
        return GlobalPhase(multiplied_phase)

    def to_qiskit(self) -> qiskit.circuit.library.GlobalPhaseGate:
        """Convert QuScalar to a Qiskit GlobalPhaseGate object."""
        return qiskit.circuit.library.GlobalPhaseGate(self.phase)

    @staticmethod
    def from_qiskit(qiskit_gate: qiskit.circuit.library.GlobalPhaseGate) -> "GlobalPhase":
        """
        Convert a Qiskit GlobalPhaseGate to a QuScalar object.
        :param qiskit_gate: Qiskit GlobalPhaseGate object
        :return: A QuScalar object
        """
        if not isinstance(qiskit_gate, qiskit.circuit.library.GlobalPhaseGate):
            raise ValueError(f"Expected GlobalPhaseGate, got {type(qiskit_gate)}.")
        phase = qiskit_gate.params[0]
        return GlobalPhase(phase)

    def to_pennylane(self) -> qml.GlobalPhase:
        """Convert QuScalar to a PennyLane GlobalPhase."""
        return qml.GlobalPhase(self.phase)

    @staticmethod
    def from_pennylane(pennylane_gate: qml.operation.Operation) -> "GlobalPhase":
        """
        Convert a PennyLane GlobalPhase to a QuScalar object.
        :param pennylane_gate: PennyLane GlobalPhase object
        :return: A QuScalar object
        """
        if not isinstance(pennylane_gate, qml.GlobalPhase):
            raise ValueError(f"Expected GlobalPhase, got {type(pennylane_gate)}.")
        phase = pennylane_gate.parameters[0]
        return GlobalPhase(phase)


class Identity(GlobalPhase):
    """No phase shift."""

    def __new__(cls) -> "Identity":
        return super().__new__(cls, 0.0)


class QuarterPhase(GlobalPhase):
    """Quarter phase shift (π/2)"""

    def __new__(cls) -> "QuarterPhase":
        return super().__new__(cls, np.pi / 2)


class HalfPhase(GlobalPhase):
    """Half phase shift (π)"""

    def __new__(cls) -> "HalfPhase":
        return super().__new__(cls, np.pi)


class ThreeQuarterPhase(GlobalPhase):
    """Three quarters phase shift (3π/2)"""

    def __new__(cls) -> "ThreeQuarterPhase":
        return super().__new__(cls, 3 * np.pi / 2)


class FullPhase(GlobalPhase):
    """Full phase shift (2π)"""

    def __new__(cls) -> "FullPhase":
        return super().__new__(cls, 2 * np.pi)
