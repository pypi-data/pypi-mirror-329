import numpy as np

from .base import QupentGate


class QupentI(QupentGate):
    """Identity gate for qupents."""

    def __new__(cls):
        obj = super().__new__(cls, np.eye(5))
        return obj


class QupentX(QupentGate):
    """X gate for qupents."""

    def __new__(cls):
        obj = super().__new__(cls, np.array([[0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]))
        return obj


class QupentZ(QupentGate):
    """Z gate for qupents."""

    def __new__(cls):
        d = 5
        omega = np.exp(2j * np.pi / d)
        phases = [omega**k for k in range(d)]
        obj = super().__new__(cls, np.diag(phases))
        return obj


class QupentH(QupentGate):
    """Hadamard gate for qupents."""

    def __new__(cls):
        obj = super().__new__(
            cls,
            np.array(
                [
                    [1, 1, 1, 1, 1],
                    [1, np.exp(2j * np.pi / 5), np.exp(4j * np.pi / 5), np.exp(6j * np.pi / 5), np.exp(8j * np.pi / 5)],
                    [1, np.exp(4j * np.pi / 5), np.exp(8j * np.pi / 5), np.exp(2j * np.pi / 5), np.exp(6j * np.pi / 5)],
                    [1, np.exp(6j * np.pi / 5), np.exp(2j * np.pi / 5), np.exp(8j * np.pi / 5), np.exp(4j * np.pi / 5)],
                    [1, np.exp(8j * np.pi / 5), np.exp(6j * np.pi / 5), np.exp(4j * np.pi / 5), np.exp(2j * np.pi / 5)],
                ]
            )
            / np.sqrt(5),
        )
        return obj


class QupentT(QupentGate):
    """T gate for qupents."""

    def __new__(cls):
        phases = [np.exp(1j * k * np.pi / 10) for k in range(5)]
        obj = super().__new__(cls, np.diag(phases))
        return obj
