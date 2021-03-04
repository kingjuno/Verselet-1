from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from compling.unsupervisedLearning.unsupervised_learning import UnsupervisedLearning
from typing import Callable, Union, Tuple


class Linkage(UnsupervisedLearning):
    """
    Hierarchical clustering is a method of cluster analysis which seeks to build a hierarchy of clusters.
    """

    def run(self, method: str = 'complete', metric: Union[str, Callable[[object], float]] = 'euclidean',
            optimal_ordering: bool = False) -> object:
        """
        Runs the hierarchical clustering for the input vectors

        Args:
            method (str, optional, default=complete): Methods for calculating the distance between the newly formed cluster u and each v. <br/> See https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html . <br/> Method can be ['complete', 'single', 'average', 'weighted', 'centroid', 'median', 'ward']
            metric (Union[str, Callable[[object], float]], optional, default=euclidean): Metricstr or function. <br/> The distance metric to use on the collection of vectors. <br/> See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html#scipy.spatial.distance.pdist for a list of valid distance metrics. A custom distance function can also be used.
            optimal_ordering (bool, optional, default=False): If True, the linkage matrix will be reordered so that the distance between successive leaves is minimal. <br/> This results in a more intuitive tree structure when the data are visualized. <br/> Default to False, because this algorithm can be slow, particularly on large datasets

        Returns:
            object: The hierarchical clustering encoded as a linkage matrix. <br/> See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
        """

        self.dendogram = hierarchy.linkage(self.data.T, method)
        self.method = method

        return self.dendogram

    def plot(self, figsize: Tuple[int, int] = (10, 12), save: str = None,
             **kwargs) -> None:
        """
        Plots the hierarchical clustering result.

        Args:
            figsize (Tuple[int, int], optional, default=10,12): Figure size: width, height in inches.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with a output name if you want save it.
            kwargs (object, optional): See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html .
        """

        if not 'labels' in kwargs:
            kwargs['labels'] = self.data.T.index
        if not 'leaf_rotation' in kwargs:
            kwargs['leaf_rotation'] = 0
        if not 'orientation' in kwargs:
            kwargs['orientation'] = 'right'
        if not 'leaf_font_size' in kwargs:
            kwargs['leaf_font_size'] = 12

        fig, ax = plt.subplots(figsize=figsize)

        dn = hierarchy.dendrogram(self.dendogram, ax=ax, **kwargs)

        plt.tight_layout()

        if save:
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

        plt.close()
