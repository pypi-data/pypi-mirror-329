# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=missing-module-docstring

from qiskit.circuit.quantumcircuit import QuantumCircuit


def clifford_2_1():
    """
    Clifford template 2_1:

    .. code-block:: text

        q_0: ─■──■─
              │  │
        q_1: ─■──■─

    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.cz(0, 1)
    qc.cz(0, 1)
    return qc
