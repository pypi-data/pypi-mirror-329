import qiskit
import pytest
import numpy as np
import pennylane as qml

from skq.base import Operator


def test_operator():
    # Pauli X Gate
    gate = Operator([[0, 1], [1, 0]])
    assert gate.dtype == complex, "Gate should be complex"
    assert gate.num_levels() == 2, "Gate should have 2 levels"
    assert gate.is_square(), "Gate should be square"
    assert gate.is_power_of_n_shape(2), "Gate shape should be a power of 2"
    assert gate.is_2d(), "Gate should be 2D"
    assert gate.is_at_least_nxn(1), "Gate should be at least 1x1"
    assert gate.is_at_least_nxn(2), "Gate should be at least 2x2"
    assert gate.is_hermitian(), "X Gate should be Hermitian"
    assert not gate.is_identity(), "X Gate should not be the identity"
    assert gate.is_equal(gate), "Gate should be equal to itself"
    assert gate.is_equal(Operator([[0, 1], [1, 0]])), "is_equal with itself should be True"
    trace = gate.trace()
    assert trace == 0, "Trace of X Gate should be 0"
    assert isinstance(trace, complex), "Trace should be a complex number"
    assert gate.frobenius_norm() == np.sqrt(2), "Frobenius norm of X Gate should be sqrt(2)"
    # Hermitian -> Eigenvalues are real
    np.testing.assert_array_almost_equal(gate.eigenvalues(), [-1.0, 1.0])
    np.testing.assert_array_almost_equal(gate.eigenvectors(), [[-1, 1], [1, 1]] / np.sqrt(2))

    zero_state = np.array([1, 0])
    assert np.allclose(gate(zero_state), np.array([0, 1])), "X Gate should encode the zero state into the one state"
    assert np.allclose(gate.encodes(zero_state), np.array([0, 1])), "X Gate should encode the zero state into the one state"
    assert np.allclose(gate.decodes(np.array([0, 1])), zero_state), "X Gate should decode the one state into the zero state"

    with pytest.raises(NotImplementedError):
        gate.to_qiskit()
    with pytest.raises(NotImplementedError):
        gate.to_pennylane()
    with pytest.raises(NotImplementedError):
        gate.from_qiskit(qiskit_operator=qiskit.circuit.library.XGate())
    with pytest.raises(NotImplementedError):
        gate.from_pennylane(pennylane_operator=qml.PauliX(wires=0))


def test_invalid_operator():
    # Empty array
    with pytest.raises(AssertionError):
        Operator(np.array([[], []]))
    # Not square
    with pytest.raises(AssertionError):
        Operator(np.array([[1, 0, 0], [0, 1, 0]]))
    # Not 2D
    with pytest.raises(AssertionError):
        Operator(np.array([1, 0, 0]))
    # Not power of 2 shape
    with pytest.raises(AssertionError):
        Operator(np.array([[1, 0], [0, 1], [0, 0], [0, 0]]))
