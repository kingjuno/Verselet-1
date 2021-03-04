from sklearn.cluster import KMeans as KM
from compling.unsupervisedLearning.unsupervised_learning import UnsupervisedLearning
from collections import defaultdict
from typing import *

class KMeans(UnsupervisedLearning):
    """
    Kmeans algorithm is an iterative algorithm that tries to partition the dataset into K pre-defined distinct non-overlapping subgroups (clusters) where each data point belongs to only one group.
    """

    def run(self, k:int, **kwargs:object) -> Dict[int, List[str]]:
        """
        Runs KMeans clustering.

        Args:
            k (int): The number of clusters to form as well as the number of centroids to generate.
            kwargs (object, optional): See https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html .

        Returns:
            Dict[int, List[str]]: Id of the clusters as keys, id of the vectors belonging in those cluster as values. <br/> The id of the cluster are automatically generated as progressive int.

                    Example:
                    >> k = KMeans(vectors, grouped_by_field="doc_id")
                    >> print(k.run(4))
                     {
                        0: [id_vector1, id_vector1, id_vector10, id_vector15, ...]
                        ...
                        3: [id_vector2, id_vector3, id_vector6, id_vector14, ...]
                     }
        """

        kwargs['n_clusters'] = k
        kmeans = KM(**kwargs)
        self.clusters = kmeans.fit_predict(self.data.T.values)

        cluster = defaultdict(list)

        data = {}
        for i, c in enumerate(self.clusters):
            cluster[c].append(self.data.T.index[i])
        for c, labels in cluster.items():
            data[str(c)] = labels

        return data