import numpy as np
import pandas as pd
from typing import *
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances


class VSM:
    """
    _Vector Space Model_ is an algebraic model for representing text documents as vectors of index terms.

    A VSM object allow you to easily explore the multi dimensional Vector Space.

    It is required that you have already performed the Vectorization.
    """

    def __init__(self, vectors: Iterable[dict], grouped_by_field: str, date_field=None) -> None:
        """
        **\_\_init\_\_**: Creates a new VSM object.

        Args:
            vectors (Iterable[dict]): Vector records produced by vectorization. <br/> Each record must have a "bow" (Bag of Words) field in which is stored a Dict[str, int]. It has tokens as key and frequencies as values.
            grouped_by_field (Union[str, List[str]]): The fields which the tokens have been grouped by (e.g. doc_id, sent_id, metada1, ...).
            date_field (str, optional, default=None): The field containing a date that refers to vectors (e.g. could be a 'publication_date' metadata). <br/> If not None, the data will be sorted by date_value.
        """

        if isinstance(grouped_by_field, str):
            self.grouped_by_field = [grouped_by_field]
        else:
            self.grouped_by_field = grouped_by_field

        self.grouped_by_field_key = " + ".join([g+'_' for g in self.grouped_by_field])
        self.date_field = date_field if date_field is None else date_field + '_'

        # dbmanager for transparent database management
        self.vectors = vectors

        # DataFrame conteining data
        self.data = {}
        for record in vectors:
            if date_field:
                self.data[record[self.grouped_by_field_key]] = dict(record['bow'], id_date=record[self.date_field])
            else:
                self.data[record[self.grouped_by_field_key]] = dict(record['bow'])
        self.data = pd.DataFrame.from_dict(self.data)

        # Replace nan with 0
        self.data.fillna(0, inplace=True)

        if date_field:
            # Sort by date_field
            self.data = self.data.T.sort_values('id_date', ascending=False)
            self.data = self.data.sort_values('id_date', axis=0)
            del self.data['id_date']

        self.distance_ = None

    def distance(self, metric: Union[str, Callable[[np.ndarray, np.ndarray], float], np.array] = "cosine") -> object:
        """
        Calculates the vector distance matrix between vectors.

        Args:

            metric (Union[str, callable], default==cosine): You can choose a metric from from sklearn.metrics.pairwise import pairwise_distances. <br/> See https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html <br/><br/> You can also pass a function too.

                       def metric(np.array, np.array) -> np.array

        Returns:
            DataFrame: Distance matrix.
        """
        if type(metric) is str:
            metric = pairwise_distances(self.data.T, self.data.T, metric=metric)
        else:
            metric = metric(self.data.T, self.data.T)

        self.distance_ = pd.DataFrame(metric, index=self.data.T.index, columns=self.data.T.index)
        return self.distance_

    def plot(self, figsize: Tuple[int, int] = (10, 10), title: str = None, save:str=None) -> None:
        """
        Plot the distance matrix as a hitmap.

        Args:
            figsize (Tuple[int, int], optional, default=10, 10): Figure size: width, height in inches.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with an output name if you want save it.
            title (str, optional, default=None):  If not None, draws title string on the figure.
        """

        if not hasattr(self, 'distance_'):
            self.distance()

        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(self.distance_)

        ax.set_xticks(np.arange(self.distance_.shape[0]))
        ax.set_yticks(np.arange(self.distance_.shape[0]))
        ax.set_xticklabels(self.distance_.index, rotation=90)
        ax.set_yticklabels(self.distance_.index)

        if title is not None:
            plt.title(title)

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

        plt.close()

    def topn(self, n: int = 10) -> Dict[str, Dict[str, float]]:
        """
        Returns the top N frequency values for each different self.grouped_by_field values.

        Args:
            n (int, optional, default=10): It will be returned the top 'n' values.

        Returns:
            Dict[str, Dict[str, float]]: grouped_by_field values as keys, frequency dict as values.

                    Example:
                    gropued_by_field = ['para_id', 'author']; n = 10

                    {
                     "para_1 + author1": {
                                         token1: 1.2,
                                         ...,
                                         token10: 0.01
                                        },
                     ...,
                     "para_151 + author1": {
                                         token1: 1.6,
                                         ...,
                                         token10: 0.5
                                        },
                     ...,
                     }
        """

        data = self.data.to_dict()

        topn = {}
        for key, value in data.items():
            topn[key] = dict(sorted(value.items(), key=lambda x: x[1], reverse=True)[:n])

        return topn