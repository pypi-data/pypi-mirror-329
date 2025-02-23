import numpy as np


def _check_quantum_state_array(X):
    """Ensure that input are normalized state vectors of the right size."""
    if len(X.shape) != 2:
        raise ValueError("Input must be a 2D array.")

    # Check if all inputs are complex
    if not np.iscomplexobj(X):
        raise ValueError("Input must be a complex array.")

    # Check if input is normalized.
    normalized = np.allclose(np.linalg.norm(X, axis=-1), 1)
    if not normalized:
        not_normalized = X[np.linalg.norm(X, axis=-1) != 1]
        raise ValueError(f"Input state vectors must be normalized. Got non-normalized vectors: '{not_normalized}'")

    # Check if input is a valid state vector
    _, n_states = X.shape
    num_qubits = int(np.log2(n_states))
    assert n_states == 2**num_qubits, f"Expected state vector length {2**num_qubits}, got {n_states}."
    return True


def to_bitstring(arr: np.array) -> list[str]:
    """
    Convert a 2D binary array to a list of bitstrings.
    :param arr: A 2D binary array
    For example:
    [[0, 1],
     [1, 0]]
    :return: List of bitstrings
    For example:
    ['01', '10']
    """
    return ["".join(map(str, m)) for m in arr]
