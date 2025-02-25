import random

def make_symmetry(CG_edges, CG_edges_weights):
    CG_edges2 = CG_edges.copy()
    CG_edges_weights2 = CG_edges_weights.copy()
    items = list(CG_edges_weights2.items())
    for pair, w in items:
        pair2 = (pair[1], pair[0])
        if pair2 not in CG_edges_weights2:
            CG_edges2.append(pair2)
            CG_edges_weights2[pair2] = w // 2
    return CG_edges2, CG_edges_weights2

def evaluate_partition(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights, partition):
    """Evaluate partition score as max partition index + sum of cut edges with weights + max partition group weight."""
    edge_cut = 0
    partition_groups = {}

    for node1, node2 in CG_edges:
        if partition[CG_nodes.index(node1)] != partition[CG_nodes.index(node2)]:
            edge_cut += CG_edges_weights.get((node1, node2), 1)

    for i, node in enumerate(CG_nodes):
        if partition[i] in partition_groups:
            partition_groups[partition[i]] += CG_nodes_weights[node]
        else:
            partition_groups[partition[i]] = CG_nodes_weights[node]
    max_partition_weight = max(partition_groups.values())

    return edge_cut + max_partition_weight


def generate_graph(no:int, ne:float, minn:int=0, maxn:int=100, mine:int=0, maxe:int=100)->'networkx.Graph':
    """Generate a random NetworkX graph with node and edge weights.
    no: number of nodes
    ne: mean number of neighbors per nodes
    minn, maxn: min and max node weight (uniformly distributed)
    mine, maxe: min and max edge weight (uniformly distributed)
    return: networkx graph
    """
    import networkx as nx
    #G = nx.binomial_graph(no, float(ne) / no)
    p = ne / (no - 1.)
    G = nx.erdos_renyi_graph(no, p)

    # Assign random weights to nodes
    for node in G.nodes:
        G.nodes[node]["weight"] = random.randint(minn, maxn)

    # Assign random weights to edges
    for edge in G.edges:
        G[edge[0]][edge[1]]["weight"] = random.randint(mine, maxe) #TODO: pymetis is only compatiable with integers

    return G

def fast_generate_graph(no:int, ne:float, minn:int=0, maxn:int=100, mine:int=0, maxe:int=100)->'networkx.Graph':
    import igraph as ig
    import networkx as nx

    p = float(ne) / no  # Probability for edge creation (sparse graph)
    g = ig.Graph.Erdos_Renyi(n=no, p=p, directed=False)
    g.es['weight'] = [random.randint(minn, maxn) for _ in range(g.ecount())]
    g.vs['weight'] = [random.randint(minn, maxn) for _ in range(g.vcount())]
    #edges = g.get_edgelist()  # Get list of edges
    #weights = g.es['weight']  # Edge weights
    nx_g = nx.Graph()
    # Add nodes to the NetworkX graph
    for node in g.vs:
        node_id = node.index  # Node index from igraph
        nx_g.add_node(node_id, weight=node['weight'])

    # Add edges to the NetworkX graph
    for edge in g.es:
        source = edge.source
        target = edge.target
        weight = edge['weight']
        nx_g.add_edge(source, target, weight=weight)
    return nx_g

def from_networkx_to_cg(G):
    """Convert a NetworkX graph into required data structures."""
    CG_nodes = [str(node) for node in G.nodes]
    CG_edges = [(str(u), str(v)) for u, v in G.edges]
    CG_edges_weights = {(str(u), str(v)): G[u][v]["weight"] for u, v in G.edges}
    CG_nodes_weights = {str(node): G.nodes[node]["weight"] for node in G.nodes}

    return CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights

def from_cg_to_networkx(CG_nodes, CG_edges, CG_edges_weights, CG_nodes_weights):
    """Convert back from custom graph structures to a NetworkX graph."""
    import networkx as nx
    G = nx.Graph()

    for node in CG_nodes:
        G.add_node(node, weight=CG_nodes_weights[node])

    for u, v in CG_edges:
        weight = CG_edges_weights[(u, v)]
        G.add_edge(u, v, weight=weight)
    return G

def plot_graph(G,partition_map=None):
    from matplotlib import pyplot as plt
    import networkx as nx

    pos = nx.shell_layout(G)

    if partition_map:
        # Use a light colormap for partitions
        unique_partitions = list(set(partition_map))
        color_map = plt.get_cmap('Pastel1', len(unique_partitions))  # Light pastel colors
        node_colors = [color_map(unique_partitions.index(partition)) for partition in partition_map]
    else:
        node_colors = 'lightgrey'  # Default color
    nx.draw(G, pos, node_color=node_colors, edge_color='grey', with_labels=False)

    node_weights = {node: G.nodes[node]["weight"] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_weights,  font_color='black')

    # Draw edge labels (weights)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

    plt.tight_layout()
    plt.show()

"""
import networkx
import random
random.seed(0)
G = generate_graph(10, 4) # takes (10000,8) takes 5min 5
part=[0,1,2, 2,2,2 ,2,3,4, 4]
plot_graph(G, part)
"""