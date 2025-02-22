# %%
import math
from typing import Any

# %%
import networkx as nx
from bloqade import qasm2
from kirin.dialects import py, ilist

# %%
# Define the problem instance as a MaxCut problem on a graph
pi = math.pi
N = 64
G = nx.random_regular_graph(3, N, seed=42)


# %%
def qaoa_sequential(G):

    edges = list(G.edges)
    nodes = list(G.nodes)

    @qasm2.extended
    def kernel(gamma: ilist.IList[float, Any], delta: ilist.IList[float, Any]):
        qreg = qasm2.qreg(len(nodes))
        for i in range(N):
            qasm2.h(qreg[i])

        for i in range(len(gamma)):
            for j in range(len(edges)):
                edge = edges[j]
                qasm2.cx(qreg[edge[0]], qreg[edge[1]])
                qasm2.rz(qreg[edge[1]], gamma[i])
                qasm2.cx(qreg[edge[0]], qreg[edge[1]])

            for j in range(N):
                qasm2.rx(qreg[j], delta[i])

        return qreg

    return kernel


# %%
def qaoa_simd(G):

    left_ids = ilist.IList([edge[0] for edge in G.edges])
    right_ids = ilist.IList([edge[1] for edge in G.edges])
    nodes = list(G.nodes)

    @qasm2.extended
    def parallel_h(qargs: ilist.IList[qasm2.Qubit, Any]):
        qasm2.parallel.u(qargs=qargs, theta=pi / 2, phi=0.0, lam=pi)

    @qasm2.extended
    def parallel_cx(
        ctrls: ilist.IList[qasm2.Qubit, Any], qargs: ilist.IList[qasm2.Qubit, Any]
    ):
        parallel_h(qargs)
        qasm2.parallel.cz(ctrls, qargs)
        parallel_h(qargs)

    @qasm2.extended
    def parallel_cz_phase(
        ctrls: ilist.IList[qasm2.Qubit, Any],
        qargs: ilist.IList[qasm2.Qubit, Any],
        gamma: float,
    ):
        parallel_cx(ctrls, qargs)
        qasm2.parallel.rz(qargs, gamma)
        parallel_cx(ctrls, qargs)

    @qasm2.extended
    def kernel(gamma: ilist.IList[float, Any], beta: ilist.IList[float, Any]):
        qreg = qasm2.qreg(len(nodes))

        def get_qubit(x: int):
            return qreg[x]

        ctrls = ilist.map(fn=get_qubit, collection=left_ids)
        qargs = ilist.map(fn=get_qubit, collection=right_ids)
        all_qubits = ilist.map(fn=get_qubit, collection=range(N))

        parallel_h(all_qubits)
        for i in range(len(gamma)):
            parallel_cz_phase(ctrls, qargs, gamma[i])
            qasm2.parallel.u(all_qubits, beta[i], 0.0, 0.0)

        return qreg

    return kernel


# %%
print("--- Sequential ---")
qaoa_sequential(G).code.print()

# %%
kernel = qaoa_simd(G)

print("\n\n--- Simd ---")
kernel.print()


# %%
@qasm2.extended
def main():
    kernel([0.1, 0.2], [0.3, 0.4])


# %%
target = qasm2.emit.QASM2(
    main_target=qasm2.main.union([qasm2.dialects.parallel, ilist, py.constant])
)
ast = target.emit(main)
qasm2.parse.pprint(ast)
