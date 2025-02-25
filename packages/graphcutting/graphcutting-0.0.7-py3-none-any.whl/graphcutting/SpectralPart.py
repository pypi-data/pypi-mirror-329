from graphcutting.util import from_cg_to_networkx


class SpectralPart:
    def __init__(self):
        pass

    def part(self, cgn, cge, cgew, cgnw, parts):
        from scipy.sparse.csgraph import laplacian
        from scipy.sparse.linalg import eigsh
        from numpy import argmin
        import networkx as nx

        G = from_cg_to_networkx(cgn, cge, cgew, cgnw)

        # Compute the normalized Laplacian matrix
        L = laplacian(nx.to_scipy_sparse_array(G), normed=True)

        # Compute the k smallest eigenvectors
        _, eigvecs = eigsh(L, k=parts, which="SM")

        # Assign clusters based on eigenvectors
        clusters = argmin(eigvecs, axis=1)

        return clusters

    def get_name(self):
        return "spectral_partition"