import numpy as np
from sklearn.cluster import DBSCAN


def GetLabels(data, eps=0.25, min_samples=10):
    values = np.array([np.array([data[i][1], data[i][0]]) for i in range(len(data))])
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(values)
    return db.labels_
