import random
import unittest
from graphcutting.util import generate_graph, fast_generate_graph

class TestRandomGraph(unittest.TestCase):
    def test_networkx_graph_generation(self):
        random.seed(1)
        no = 10
        ne = 2.
        nx_g = generate_graph(no, ne)
        no_out = len(nx_g.nodes)
        ne_out = len(nx_g.edges)
        self.assertEqual(no_out, no)

        """
        Edge probability model: Binomial: n = 100, p = 0.2

        Mean: np = 100 * 0.2 = 20

        Std: \sqrt{np(1 - p)} = \sqrt{100 \times 0.2 \times 0.8} = \sqrt{16} = 4

        Boundary for 0.999 confidence:
        The z-score for 0.999 confidence is ~3.
        The boundary becomes:
        20 +- (3 \times 4) -> 8 and 32

        """
        self.assertTrue(32 > ne_out > 8)

    def test_igraph_graph_generation(self):
        random.seed(0)
        no = 10
        ne = 2.
        nx_g = fast_generate_graph(no, ne)
        no_out = len(nx_g.nodes)
        ne_out = len(nx_g.edges)
        self.assertEqual(no_out, no)

        """
        Edge probability model: Binomial: n = 100, p = 0.2

        Mean: np = 100 * 0.2 = 20

        Std: \sqrt{np(1 - p)} = \sqrt{100 \times 0.2 \times 0.8} = \sqrt{16} = 4

        Boundary for 0.999 confidence:
        The z-score for 0.999 confidence is ~3.
        The boundary becomes:
        20 +- (3 \times 4) -> 8 and 32

        """
        self.assertTrue(32 > ne_out > 8)

