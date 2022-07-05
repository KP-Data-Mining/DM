import umap as u

def CompressingData(data, n_neighbors=5, min_dist=0.1, n_components=2):
    embedding = u.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components).fit_transform(data)
    return embedding
