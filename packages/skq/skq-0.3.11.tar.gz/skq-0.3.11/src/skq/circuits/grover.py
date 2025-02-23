import numpy as np

from ..gates.qubit.multi import PhaseOracle, GroverDiffusion
from ..gates.qubit.single import H, Measure
from .circuit import Circuit, Concat


class Grover:
    """
    Grover's search algorithm.
    """

    def get_grover_circuit(self, target_state: np.array, n_qubits: int, n_iterations: int, measure: bool = True) -> Circuit:
        """
        :param target_state: Target state to search for.
        :param n_qubits: Number of qubits in the circuit.
        :param n_iterations: Number of Grover iterations to perform.
        :param measure: Whether to measure the qubits.
        :return: Circuit for the Grover search algorithm.
        """
        single_grover_iteration = [PhaseOracle(target_state), GroverDiffusion(n_qubits=n_qubits)]
        equal_superposition = Concat([H() for _ in range(n_qubits)])
        steps = [equal_superposition, *[gate for _ in range(n_iterations) for gate in single_grover_iteration]]
        if measure:
            steps.append(Measure())
        return Circuit(steps)
