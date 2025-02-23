import numpy as np

from .base import QuquartGate


class QuquartI(QuquartGate):
    """Identity gate for ququarts."""

    def __new__(cls):
        obj = super().__new__(cls, np.eye(4))
        return obj


class QuquartX(QuquartGate):
    """X gate for ququarts."""

    def __new__(cls):
        obj = super().__new__(cls, np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]))
        return obj


class QuquartZ(QuquartGate):
    """Z gate for ququarts."""

    def __new__(cls):
        obj = super().__new__(cls, np.array([[1, 0, 0, 0], [0, 1j, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1j]]))
        return obj


class QuquartH(QuquartGate):
    """Hadamard gate for ququarts."""

    def __new__(cls):
        obj = super().__new__(cls, np.array([[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]]) / 2)
        return obj


class QuquartT(QuquartGate):
    """T gate for ququarts."""

    def __new__(cls):
        obj = super().__new__(cls, np.diag([1, np.exp(1j * np.pi / 4), 1, 1]))
        return obj
