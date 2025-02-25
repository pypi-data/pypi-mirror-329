from itertools import combinations, islice

from graphcutting.util import from_cg_to_networkx

class GirvanNewmanPart:
    def __init__(self):
        pass

    def compute_community_cost(self, G, community):
        """Compute the total cost of a community as the sum of node weights."""
        return sum(G.nodes[n]['weight'] for n in community)

    def compute_edge_cut_cost(self, G, comm1, comm2):
        """Compute the total edge weight between two communities."""
        return sum(G[u][v]['weight'] for u in comm1 for v in comm2 if G.has_edge(u, v))

    def merge_best_communities(self, G, communities, target_k):
        """
        Merges communities to minimize max(community cost) + edge cut cost.

        Parameters:
        - G: The original NetworkX graph with node and edge weights.
        - communities: List of sets, each containing nodes of a community.
        - target_k: The exact number of clusters required.

        Returns:
        - List of `target_k` sets of nodes.
        """
        while len(communities) > target_k:
            best_merge = None
            min_score = float("inf")

            for c1, c2 in combinations(communities, 2):
                cost1, cost2 = self.compute_community_cost(G, c1), self.compute_community_cost(G, c2)
                edge_cut = self.compute_edge_cut_cost(G, c1, c2)

                new_cost = cost1 + cost2  # New community cost after merging
                max_cost = max(new_cost,
                               max(self.compute_community_cost(G, c) for c in communities if c != c1 and c != c2))

                score = max_cost + edge_cut  # Optimization metric

                if score < min_score:
                    min_score = score
                    best_merge = (c1, c2)

            if best_merge:
                # Merge the two selected communities
                communities.remove(best_merge[0])
                communities.remove(best_merge[1])
                communities.append(best_merge[0] | best_merge[1])  # Union of sets

        return communities

    def part(self, cgn, cge, cgew, cgnw, parts):
        """
        Performs Girvan-Newman clustering with weighted merging.

        Parameters:
        - cgn: List of node IDs
        - cge: List of edges (tuples)
        - cgew: List of edge weights
        - cgnw: List of node weights
        - parts: Desired number of partitions (clusters)

        Returns:
        - List of cluster assignments for each node.
        """
        from networkx.algorithms.community import girvan_newman

        G = from_cg_to_networkx(cgn, cge, cgew, cgnw)

        # Generate hierarchical clustering using Girvan-Newman
        comp = girvan_newman(G)

        partition = None
        try:
            partition = next(islice(comp, parts - 1, parts))
        except StopIteration:
            partition = list(next(comp))  # Fallback to the last available split

        # If too many clusters, merge intelligently
        if len(partition) > parts:
            partition = self.merge_best_communities(G, list(partition), parts)

        # Assign cluster labels
        cluster_map = {}
        for i, community in enumerate(partition):
            for node in community:
                cluster_map[node] = i

        # Convert to a list with node order (partition ID)
        clusters = [cluster_map[node] for node in cgn]

        return clusters

    def get_name(self):
        return "girvan_newman"