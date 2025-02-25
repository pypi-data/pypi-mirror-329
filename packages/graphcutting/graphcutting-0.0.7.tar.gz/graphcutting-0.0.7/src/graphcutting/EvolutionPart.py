import random
import multiprocessing

from graphcutting.util import evaluate_partition

def generate_random_partition(CG_nodes, parts):
    """Generate a random partitioning of nodes."""
    return [random.randint(0, parts - 1) for _ in CG_nodes]


def mutate_partition(best_partition, parts, mutation_rate=0.1,):
    """Mutate the best partition by randomly changing partitions for some nodes."""
    new_partition = best_partition[:]
    for i in range(len(new_partition)):
        if random.random() < mutation_rate:
            new_partition[i] = random.randint(0, parts - 1)
    return new_partition



def pop_random(args:tuple):
    CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts, i = args
    candidate=generate_random_partition(CG_nodes, parts)
    scored_population = evaluate_partition(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, candidate)
    return scored_population, candidate

def pop_mutation(args:tuple):
    CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, partition_parent, mutation_rate, parts,  i = args
    mutated_candidate = mutate_partition(partition_parent, parts, mutation_rate=mutation_rate)
    scored_population = evaluate_partition(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, mutated_candidate)
    return scored_population, mutated_candidate

def _evolutionary_part(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts,
                       generations=20,
                       population_size=1000, procs=20, init_mutation_rate = 0.5, mutation_decay=0.5):
    """Perform evolutionary graph partitioning using multiprocessing."""
     #, 0.25, 0.125, 0.06125, 0.03, 0.015, 0.0075, ..

    # Function to initialize random seeds for each worker

    # Generate the population and evaluate
    with multiprocessing.Pool(procs) as pool:
        scored_population = pool.map(pop_random,
                                     [(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts, i) for i in range(population_size)])

    scored_population.sort()
    best_score, best_partition = scored_population[0]

    #best_partition = generate_random_partition(CG_nodes, parts)
    #best_score = evaluate_partition(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, best_partition)

    #print(f"Generation 0: Best Score = {best_score}")

    # Step 2: Evolutionary loop
    for gen in range(1, generations + 1):

        # Regenerate the mutated population with unique seeds
        with multiprocessing.Pool(procs) as pool:
            scored_population = pool.map(pop_mutation,
                                         [(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, best_partition, init_mutation_rate, parts, i) for i in
                                          range(population_size)])

        scored_population.sort()
        scored_best_score, scored_best_partition = scored_population[0]

        if scored_best_score < best_score:
            best_score = scored_best_score
            best_partition = scored_best_partition
        else:
            init_mutation_rate= init_mutation_rate * mutation_decay

        #print(f"Generation {gen}: Best Score = {best_score} among {len(scored_population)}")

    return best_partition


class EvolutionPart:
    def __init__(self,generations=20,
                       population_size=1000, procs=20, init_mutation_rate = 0.5, mutation_decay=0.5):
        self.generations=generations
        self.population_size=population_size
        self.procs=procs
        self.init_mutation_rate=init_mutation_rate
        self.mutation_decay=mutation_decay

    def part(self,CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts) -> list[int]:
        partitioning=_evolutionary_part(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights,
                                        parts=parts,
                                        procs=self.procs,
                                        population_size=self.population_size,
                                        init_mutation_rate=self.init_mutation_rate,
                                        mutation_decay=self.mutation_decay
                                        )
        return partitioning

    def get_name(self):
        return f"evol_gen{self.generations}_pop{self.population_size}_mut{self.init_mutation_rate}"
