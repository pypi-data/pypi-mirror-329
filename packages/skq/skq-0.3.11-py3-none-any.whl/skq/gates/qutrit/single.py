import numpy as np

from .base import QutritGate


class QutritI(QutritGate):
    """
    Identity gate for a qutrit.
    [[1, 0, 0]
    [0, 1, 0]
    [0, 0, 1]]
    """

    def __new__(cls):
        return super().__new__(cls, np.eye(3))


class QutritX(QutritGate):
    """
    X gate for a qutrit.
    |0> -> |1>
    |1> -> |2>
    |2> -> |0>
    """

    def __new__(cls):
        return super().__new__(cls, np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]))


class QutritY(QutritGate):
    """
    Y gate for a qutrit.
    |0> -> -i|1>
    |1> -> -i|2>
    |2> -> -i|0>
    """

    def __new__(cls):
        return super().__new__(cls, np.array([[0, 0, -1j], [-1j, 0, 0], [0, -1j, 0]]))


class QutritZ(QutritGate):
    """
    Z gate for a qutrit.
    |0> -> |0>
    |1> -> exp(2*pi*i/3)|1>
    |2> -> exp(-2*pi*i/3)|2>
    """

    def __new__(cls):
        return super().__new__(cls, np.array([[1, 0, 0], [0, np.exp(2 * np.pi * 1j / 3), 0], [0, 0, np.exp(-2 * np.pi * 1j / 3)]]))


class QutritH(QutritGate):
    """
    Hadamard gate for a qutrit.
    |0> -> (|0> + |1> + |2>)/sqrt(3)
    |1> -> (|0> + e^(2πi/3)|1> + e^(4πi/3)|2>)/sqrt(3)
    |2> -> (|0> + e^(4πi/3)|1> + e^(2πi/3)|2>)/sqrt(3)
    """

    def __new__(cls):
        omega = np.exp(2j * np.pi / 3)
        return super().__new__(cls, np.array([[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]) / np.sqrt(3))


class QutritT(QutritGate):
    """
    T gate for a qutrit.
    |0> -> |0>
    |1> -> exp(2*pi*i/9)|1>
    |2> -> exp(-2*pi*i/9)|2>
    """

    def __new__(cls):
        return super().__new__(cls, np.array([[1, 0, 0], [0, np.exp(2 * np.pi * 1j / 9), 0], [0, 0, np.exp(-2 * np.pi * 1j / 9)]]))


class QutritR(QutritGate):
    """R gate for a qutrit (non-Clifford gate)."""

    def __new__(cls):
        return super().__new__(cls, np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]]))


class QutritPhase(QutritGate):
    """
    General phase gate for qutrits.
    Applies phase shifts to the qutrit basis states.
    """

    def __new__(cls, phi_0: float, phi_1: float, phi_2: float):
        return super().__new__(cls, np.array([[np.exp(1j * phi_0), 0, 0], [0, np.exp(1j * phi_1), 0], [0, 0, np.exp(1j * phi_2)]]))


class QutritS(QutritPhase):
    """
    S gate for qutrits.
    |0> -> |0>
    |1> -> exp(2*pi*i/3)|1>
    |2> -> exp(4*pi*i/3)|2>
    """

    def __new__(cls):
        return super().__new__(cls, phi_0=0, phi_1=2 * np.pi / 3, phi_2=4 * np.pi / 3)
