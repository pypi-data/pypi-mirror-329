import numpy as np
from ..base import BaseGate


class QupentGate(BaseGate):
    """
    Base class for Qupent gates.
    These are quantum systems with a basis of 5 states. |0>, |1>, |2>, |3>, |4>.
    Models spin-2 particles like the graviton.
    """

    def __new__(cls, input_array):
        obj = super().__new__(cls, input_array)
        assert obj.is_at_least_nxn(n=5), "Gate must be at least a 5x5 matrix"
        assert obj.is_power_of_n_shape(n=5), "Gate shape must be a power of 5"
        return obj

    def num_qupents(self) -> int:
        """Return the number of qupents involved in the gate."""
        return int(np.log(self.shape[0]) / np.log(5))

    def is_multi_qupent(self) -> bool:
        """Check if the gate involves multiple qupents."""
        return self.num_qupents() > 1
