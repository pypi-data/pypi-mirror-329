import numpy as np


from ..gates.qubit import X, H, Z, CX, I, RY, CH
from .circuit import Circuit, Concat


class BellStates:
    """
    Convenience class for generating Bell States as skq Pipelines.
    More information on defining Bell States:
    - https://quantumcomputinguk.org/tutorials/introduction-to-bell-states
    - https://quantumcomputing.stackexchange.com/a/2260
    """

    def get_bell_state(self, configuration: int = 1) -> Circuit:
        """
        Return circuit for the Bell State based on the configuration.
        :param configuration: Configuration of the Bell State.
        Configuration 1: |Φ+⟩ =|00> + |11> / sqrt(2)
        Configuration 2: |Φ-⟩ =|00> - |11> / sqrt(2)
        Configuration 3: |Ψ+⟩ =|01> + |10> / sqrt(2)
        Configuration 4: |Ψ-⟩ =|01> - |10> / sqrt(2)
        :return: Circuit for the Bell State.
        """
        assert configuration in [1, 2, 3, 4], f"Invalid Bell State configuration: {configuration}. Configurations are: 1: |Φ+⟩, 2: |Φ-⟩, 3: |Ψ+⟩, 4: |Ψ-⟩"
        config_mapping = {
            1: self.get_bell_state_omega_plus,
            2: self.get_bell_state_omega_minus,
            3: self.get_bell_state_phi_plus,
            4: self.get_bell_state_phi_minus,
        }
        pipe = config_mapping[configuration]()
        return pipe

    def get_bell_state_omega_plus(self) -> Circuit:
        """
        Return circuit for the entangled state |Φ+⟩ =|00> + |11> / sqrt(2).
        This corresponds to the 1st bell state.
        :return: Circuit for creating the 1st Bell State.
        """
        return Circuit([Concat([H(), I()]), CX()])

    def get_bell_state_omega_minus(self) -> Circuit:
        """
        Return circuit for the entangled state |Φ−⟩ =|00> - |11> / sqrt(2).
        This corresponds to the 2nd bell state.
        :return: Circuit for creating the 2nd Bell State

        """
        return Circuit([Concat([H(), I()]), CX(), Concat([Z(), I()])])

    def get_bell_state_phi_plus(self) -> Circuit:
        """
        Return circuit for the entangled state  |Ψ+⟩ =|01> + |10> / sqrt(2).
        This corresponds to the 3rd bell state.
        :return: Circuit for creating the 3rd Bell State
        """
        return Circuit([Concat([H(), X()]), CX()])

    def get_bell_state_phi_minus(self) -> Circuit:
        """
        Return circuit for the entangled state |Ψ−⟩ =|01> - |10> / sqrt(2).
        This corresponds to the 4th bell state.
        :return: Circuit for creating the 4th Bell State
        """
        return Circuit([Concat([H(), X()]), Concat([Z(), Z()]), CX()])


class GHZStates:
    """
    Generalization of Bell States to 3 or more qubits.
    Greenberger-Horne-Zeilinger (GHZ) states.
    """

    def get_ghz_state(self, n_qubits: int) -> Circuit:
        """
        :param n_qubits: Number of qubits in the GHZ state.
        :return: Circuit for the GHZ state.
        """
        assert n_qubits > 2, "GHZ state requires at least 3 qubits"
        return Circuit([Concat([H()] + [I()] * (n_qubits - 1)), *[Concat([I()] * i + [CX()] + [I()] * (n_qubits - i - 2)) for i in range(n_qubits - 1)]])


class WState:
    """3-qubit W State: (|001⟩ + |010⟩ + |100⟩)/√3"""

    def get_w_state(self) -> Circuit:
        theta = -2 * np.arccos(1 / np.sqrt(3))
        return Circuit(
            [
                Concat([RY(theta), I(), I()]),
                Concat([CH(), I()]),
                Concat([I(), CX()]),
                Concat([CX(), I()]),
                Concat([X(), I(), I()]),
            ]
        )
