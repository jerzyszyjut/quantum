from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator
import math


def grover_oracle_3sat(clauses, num_vars):
    """
    Creates a Grover oracle for a 3-SAT problem.

    Args:
        clauses: List of clauses, where each clause is a list of 3 integers.
                Positive integers represent positive literals (e.g., x1),
                negative integers represent negative literals (e.g., ¬x1).
        num_vars: Number of variables in the 3-SAT formula.

    Returns:
        QuantumCircuit: The oracle circuit that marks satisfying assignments.
    """
    num_clauses = len(clauses)
    total_qubits = num_vars + num_clauses + 1
    qc = QuantumCircuit(total_qubits)

    # Label registers
    assignment = list(range(num_vars))
    clause_ancillas = list(range(num_vars, num_vars + num_clauses))
    phase_qubit = total_qubits - 1

    # Prepare phase qubit in |–> state
    qc.h(phase_qubit)
    qc.x(phase_qubit)

    # For each clause, evaluate if it's satisfied
    for i, clause in enumerate(clauses):
        # Initialize clause ancilla to |0⟩
        qc.x(clause_ancillas[i])

        # For each literal in the clause
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                # For positive literals, we want to detect |1>
                qc.cx(assignment[var_index], clause_ancillas[i])
            else:
                # For negative literals, we want to detect |0>
                qc.x(assignment[var_index])
                qc.cx(assignment[var_index], clause_ancillas[i])
                qc.x(assignment[var_index])

        # Invert the clause ancilla so that |1> means clause is satisfied
        qc.x(clause_ancillas[i])

    qc.barrier()

    # If all clauses are satisfied (all clause ancillas are |1>),
    # flip the phase qubit
    qc.mcx(clause_ancillas, phase_qubit)

    qc.barrier()

    # Uncompute clause ancillas
    for i, clause in reversed(list(enumerate(clauses))):
        # Invert the clause ancilla back
        qc.x(clause_ancillas[i])

        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                qc.cx(assignment[var_index], clause_ancillas[i])
            else:
                qc.x(assignment[var_index])
                qc.cx(assignment[var_index], clause_ancillas[i])
                qc.x(assignment[var_index])

        # Reset clause ancilla to |0⟩
        qc.x(clause_ancillas[i])

    # Restore phase qubit to computational basis
    qc.x(phase_qubit)
    qc.h(phase_qubit)

    return qc


def run_grover_3sat(clauses, num_vars):
    """
    Runs Grover's algorithm on a 3-SAT problem.

    Args:
        clauses: List of clauses in the 3-SAT formula
        num_vars: Number of variables in the formula

    Returns:
        dict: Measurement counts of the results
    """
    # Create the oracle
    oracle = grover_oracle_3sat(clauses, num_vars)

    # Create the Grover operator
    grover_op = GroverOperator(oracle)

    # Calculate optimal number of iterations
    N = num_vars  # Only count the assignment qubits for iteration calculation
    optimal_num_iterations = math.floor(math.pi / (4 * math.asin(math.sqrt(1 / 2**N))))
    print(f"Optimal number of iterations: {optimal_num_iterations}")

    # Create the full circuit
    qc = QuantumCircuit(oracle.num_qubits, num_vars)
    qc.h(range(num_vars))  # Initialize only assignment qubits in equal superposition
    qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
    qc.measure(
        list(range(num_vars)), list(range(num_vars))
    )  # Measure only the assignment qubits

    # Run the circuit
    simulator = AerSimulator()
    qc_compiled = transpile(qc, simulator)
    job = simulator.run(qc_compiled, shots=1000)
    result = job.result()
    counts = result.get_counts(qc_compiled)

    return counts


if __name__ == "__main__":
    # Example: 3-SAT formula with 3 variables and 3 clauses
    # (x1 OR x2 OR x3) AND (x1 OR ¬x2 OR ¬x3) AND (¬x1 OR x2 OR ¬x3)
    # This formula has a unique satisfying assignment: x1=1, x2=1, x3=0
    clauses = [
        [1, 2, 3],  # (x1 OR x2 OR x3)
        [1, -2, -3],  # (x1 OR ¬x2 OR ¬x3)
        [-1, 2, -3],  # (¬x1 OR x2 OR ¬x3)
    ]
    num_vars = 3

    # Run Grover's algorithm
    counts = run_grover_3sat(clauses, num_vars)
    print("\nMeasurement results:")
    print(counts)

    # Plot the results
    plot_histogram(counts)
