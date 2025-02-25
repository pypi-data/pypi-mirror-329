import random
import multiprocessing
from graphcutting.util import evaluate_partition

def generate_first_partition(nnodes, parts):
    """Generate a first partitioning of nodes."""
    return [0 for _ in range(nnodes)]

def candidate_next_step_static(args) -> tuple[float, list[int]]:
    partition_parent, node_id, feature_id, cg = args
    new_partition = partition_parent[:]
    new_partition[node_id] = feature_id
    scored_population = evaluate_partition(*cg, new_partition)
    return scored_population, new_partition

class StepWisePartSeq:
    def __init__(self, cg, nnodes: int, parts: int, procs: int = 4, max_neigh_per_step: int = 30, max_steps: int = 10):
        self.cg = cg
        self.nnodes = nnodes
        self.parts = parts
        self.procs = procs
        self.max_neigh_per_step = max_neigh_per_step
        self.max_steps = max_steps

    def _first_candidate_score(self) -> tuple[float, list[int]]:
        candidate = generate_first_partition(self.nnodes, self.parts)
        scored_population = evaluate_partition(*self.cg, candidate)
        return scored_population, candidate

    def partitioning(self):
        best_score, best_partition = self._first_candidate_score()
        #print(f"Initial score: {best_score}")

        for stepid in range(self.max_steps):
            maxprocid = min(max(best_partition) + 1, self.parts - 1)
            neighbors = []
            for feature_id in range(self.nnodes):  # Scan all nodes
                for core_id in range(maxprocid + 1):
                    if best_partition[feature_id] != core_id:
                        neighbors.append((best_partition, feature_id, core_id, self.cg))

            # Subsample neighbors
            if len(neighbors) > self.max_neigh_per_step:
                neighbors = random.sample(neighbors, self.max_neigh_per_step)

            # Evaluate neighbors
            with multiprocessing.Pool(self.procs) as pool: # <---------------------------- parallelism
                scored_population = pool.map(candidate_next_step_static, neighbors)

            # Sort and select the best candidate
            scored_population.sort()
            scored_best_score, scored_best_partition = scored_population[0]

            if scored_best_score < best_score:
                best_score = scored_best_score
                best_partition = scored_best_partition
            else:
                return best_partition

        return best_partition

class StepWisePart:
    def __init__(self, max_neigh_per_step:int=200, max_steps:int=100, procs:int=20):
        self.procs = procs
        self.max_neigh_per_step=max_neigh_per_step
        self.max_steps=max_steps
        self.sw = None

    def part(self, CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts) -> list[int]:
        cg=(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights)
        self.sw = StepWisePartSeq(
            cg=cg,
            nnodes=len(CG_nodes),
            parts=parts,
            procs=self.procs
        )
        optimized_part = self.sw.partitioning()
        return optimized_part

    def get_name(self):
        return f"step_wise_neigh{self.max_neigh_per_step}_steps{self.max_steps}"
