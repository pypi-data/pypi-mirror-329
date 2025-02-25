import unittest
from graphcutting.util import evaluate_partition

def get_cg():
    CG_nodes = ["n0", "n1", "n2", "n3", "n4"]
    CG_edges = [("n0", "n1"), ("n0", "n2"), ("n1", "n2"), ("n1", "n3"), ("n2", "n3"), ("n2", "n4"),
                     ("n3", "n4")]
    CG_edges_weights = {
        ("n0", "n1"): 3.0, ("n0", "n2"): 2.5, ("n1", "n2"): 2.5,
        ("n1", "n3"): 1.2, ("n2", "n3"): 1.2, ("n2", "n4"): 2.8, ("n3", "n4"): 2.8
    }
    CG_nodes_weights = {"n0": 3, "n1": 4, "n2": 5, "n3": 6, "n4": 7}

    cg = (CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights)
    return cg

class TestGraphPartitioning(unittest.TestCase):

    def _check_strategy(self, cg, strategy, parts):
        part = strategy.part(*cg, parts)

        # Valid partition
        CG_nodes=cg[0]
        self.assertEqual(len(part), len(CG_nodes), f"{strategy.get_name()} did not cover all nodes.")
        for partid in part:
            self.assertTrue(0 <= partid < parts, f"{strategy.get_name()} node outside wanted partitions" )

        # Valid score
        score = evaluate_partition(*cg, part)
        self.assertIsInstance(score, float, f"{strategy.get_name()} did not return a valid score.")

    def test_step_wise(self):
        from graphcutting.StepWisePart import StepWisePart
        self._check_strategy(get_cg(), StepWisePart(), 2)

    def test_evolution1(self):
        from graphcutting.EvolutionPart import EvolutionPart
        self._check_strategy(get_cg(), EvolutionPart(init_mutation_rate=0.5), 2)

    def test_evolution2(self):
        from graphcutting.EvolutionPart import EvolutionPart
        self._check_strategy(get_cg(), EvolutionPart(init_mutation_rate=0.1), 2)

    def test_metis(self):
        from graphcutting.MetisPart import MetisPart
        self._check_strategy(get_cg(), MetisPart(), 2)

    def test_zoltan_parmetis(self):
        from graphcutting.ZoltanPart import ZoltanPart
        self._check_strategy(get_cg(), ZoltanPart("PARMETIS"), 2)

    def test_zoltan_scotch(self):
        from graphcutting.ZoltanPart import ZoltanPart
        self._check_strategy(get_cg(), ZoltanPart("SCOTCH"), 2)

    def test_zoltan_phg(self):
        from graphcutting.ZoltanPart import ZoltanPart
        self._check_strategy(get_cg(), ZoltanPart("PHG"), 2)

    def test_node2vec(self):
        from graphcutting.Node2VecPart import Node2VecPart
        self._check_strategy(get_cg(), Node2VecPart(), 2)

    def test_girvan(self):
        from graphcutting.GirvanNewmanPart import GirvanNewmanPart
        self._check_strategy(get_cg(), GirvanNewmanPart(), 2)

    def test_louvain(self):
        from graphcutting.LouvainPart import LouvainPart
        self._check_strategy(get_cg(), LouvainPart(), 2)

    def test_spectral(self):
        from graphcutting.SpectralPart import SpectralPart
        self._check_strategy(get_cg(), SpectralPart(), 2)

if __name__ == '__main__':
    unittest.main()