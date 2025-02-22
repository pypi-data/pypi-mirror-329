from . import _quizx
from .graph import VecGraph


def extract_circuit(g: VecGraph) -> "Circuit":
    c = Circuit()
    c._c = _quizx.extract_circuit(g.get_raw_graph())
    return c


class Circuit:
    def __init__(self):
        self._c = None

    @staticmethod
    def load(circuitfile: str) -> "Circuit":
        c = Circuit()
        c._c = _quizx.Circuit.load(circuitfile)
        return c

    @staticmethod
    def from_qasm(qasm: str) -> "Circuit":
        c = Circuit()
        c._c = _quizx.Circuit.from_qasm(qasm)
        return c

    def to_qasm(self):
        return self._c.to_qasm()

    def to_graph(self):
        g = VecGraph()
        g._g = self._c.to_graph()
        return g

    def stats(self):
        return self._c.stats()

    def __repr__(self):
        return self._c.stats().to_string()
