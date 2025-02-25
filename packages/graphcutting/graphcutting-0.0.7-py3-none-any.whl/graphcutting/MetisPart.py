def _pymetis_part(CG_nodes: list[str],
                  CG_edges: list[tuple[str,str]],
                  CG_edges_weights: dict[str, float],
                  CG_nodes_weights: dict[str, float],
                  parts: int) -> list[int]:
    import pymetis
    # Convert edge sets to adjacency list format for pymetis
    adjacency_list = [[] for _ in range(len(CG_nodes))]
    node_index = {name: i for i, name in enumerate(CG_nodes)}

    # Map for edge weights
    edge_weights_map = {}

    # Populate adjacency list and edge weights
    for edge in CG_edges:
        #for edge_set in edges:
        if len(edge) == 2:
            n1, n2 = node_index[edge[0]], node_index[edge[1]]
            adjacency_list[n1].append(n2)
            adjacency_list[n2].append(n1)

            # Assign weight for this edge
            weight = int(CG_edges_weights.get(edge, 1.0))  # Default weight = 1.0 if not provided
            edge_weights_map[frozenset((n1, n2))] = weight
        else:
            raise ValueError("partition_CG_graphV2 error. Expect 2 node IDs in the edge")

    # Flatten edge weights to align with adjacency list format
    eweights = []
    for i, neighbors in enumerate(adjacency_list):
        for neighbor in neighbors:
            w=edge_weights_map[frozenset((i, neighbor))]
            eweights.append(w)

    vweights = []
    for node_name in CG_nodes:
        vw=CG_nodes_weights[node_name]
        vweights.append(vw)

    # Perform graph partitioning with pymetis
    _, node_colors = pymetis.part_graph(parts, adjacency=adjacency_list,
                                        eweights=eweights,
                                        vweights=vweights)

    return node_colors

class MetisPart:
    def __init__(self):
        pass

    def part(self, CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts):
        return _pymetis_part(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, parts)

    def get_name(self):
        return "metis"