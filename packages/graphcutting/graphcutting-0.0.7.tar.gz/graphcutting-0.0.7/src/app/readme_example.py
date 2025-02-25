from graphcutting import EvolutionPart, MetisPart, ZoltanPart, SpectralPart, Node2VecPart, GirvanNewmanPart, StepWisePart

strategies=[]
strategies.append(StepWisePart(max_neigh_per_step=20, max_steps=10))
strategies.append(EvolutionPart(init_mutation_rate=0.25, population_size=10, generations=10))
strategies.append(MetisPart())
strategies.append(ZoltanPart("PHG"))
strategies.append(ZoltanPart("SCOTCH"))
strategies.append(ZoltanPart("PARMETIS"))
strategies.append(SpectralPart())
strategies.append(Node2VecPart(dimensions=16, num_walks=100))
strategies.append(GirvanNewmanPart())

nodes = ["n0", "n1", "n2", "n3"]
edges = [("n0", "n1"), ("n1", "n2"), ("n2", "n3"), ("n1", "n3")]
edges_weights = { ("n0", "n1"): 1, ("n1", "n2"): 1,
    ("n2", "n3"): 1, ("n1", "n3"): 1}
nodes_weights = {"n0": 100, "n1": 1, "n2": 1, "n3": 100}

for strategy in strategies:
    try:
        partitioning = strategy.part(nodes, edges, edges_weights, nodes_weights, 2)
        print(strategy.get_name(), "partitioning:", partitioning)
    except Exception as e:
        print(strategy.get_name(), "exception:" , e)
