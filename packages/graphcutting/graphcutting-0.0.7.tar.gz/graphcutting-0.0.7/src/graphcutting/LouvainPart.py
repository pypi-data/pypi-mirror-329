from graphcutting.util import from_cg_to_networkx

class LouvainPart:
    def __init__(self):
        pass

    def part(self, cgn, cge, cgew, cgnw, parts):
        import community as community_louvain

        G = from_cg_to_networkx(cgn, cge, cgew, cgnw)

        # Apply Louvain method for community detection
        partition = community_louvain.best_partition(G)

        # Convert partition dict to a list of communities
        community_map = {}
        for node, comm in partition.items():
            if comm not in community_map:
                community_map[comm] = []
            community_map[comm].append(node)

        # If more than 2 communities, merge them to form exactly 2 partitions
        if len(community_map) > parts:
            # Merge extra communities into two larger ones
            sorted_communities = sorted(community_map.values(), key=len, reverse=True)
            merged_communities = sorted_communities[:parts - 1]  # Keep largest `parts - 1` communities

            # Merge the remaining communities into one
            merged_communities.append([node for comm in sorted_communities[parts - 1:] for node in comm])

            # Re-map the nodes to the new partition
            new_partition = {}
            for i, comm in enumerate(merged_communities):
                for node in comm:
                    new_partition[node] = i
            return [new_partition[node] for node in G.nodes()]
        else:
            clusters=[]
            for n in cgn:
                partition_id=partition[n]
                clusters.append(partition_id)
        return clusters

    def get_name(self):
        return "louvain_partition"