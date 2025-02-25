from graphcutting.util import from_cg_to_networkx

class Node2VecPart:
    def __init__(self, dimensions=16, walk_length=30, num_walks=200, workers=20, window=10, min_count=1, batch_words=4, seed=42):
        self.dimensions=dimensions
        self.walk_length=walk_length
        self.num_walks=num_walks
        self.workers=workers
        self.window=window
        self.min_count=min_count
        self.batch_words=batch_words
        self.seed=seed

    def part(self, cgn, cge, cgew, cgnw, parts):
        import numpy as np
        from sklearn.cluster import KMeans
        from node2vec import Node2Vec  # pip3 install node2vec

        G = from_cg_to_networkx(cgn, cge, cgew, cgnw)

        # Generate node embeddings using Node2Vec
        node2vec = Node2Vec(G, dimensions=self.dimensions,
                            walk_length=self.walk_length,
                            num_walks=self.num_walks,
                            workers=self.workers,
                            quiet=True)

        model = node2vec.fit(window=self.window, min_count=self.min_count, batch_words=self.batch_words)

        # Get node embeddings
        embeddings = np.array([model.wv[str(node)] for node in G.nodes()])

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=parts, random_state=self.seed, n_init='auto')
        clusters = kmeans.fit_predict(embeddings)

        return clusters

    def get_name(self):
        return "node2vec_partition"