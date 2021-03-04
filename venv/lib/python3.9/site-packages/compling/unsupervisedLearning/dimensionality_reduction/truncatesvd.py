import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from sklearn import decomposition
from compling.unsupervisedLearning.unsupervised_learning import UnsupervisedLearning
from typing import Tuple


class TruncatedSVD(UnsupervisedLearning):
    """
    TruncateSVD, is a dimensionality-reduction method that is often used to reduce the dimensionality of large data sets, by transforming a large set of variables into a smaller one that still contains most of the information in the large set.
    """

    def run(self, n:int, **kwargs) -> object:
        """
        Runs TruncateSVD on input vectors.

        Args:
            n (int): Number of components to keep.
            kwargs (object): See https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncateSVD.html .

        Returns:
            object: Performed dimensionality reduction on input vectors. <br/> See https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncateSVD.html
        """

        truncatesvd = decomposition.TruncatedSVD(n_components=n)
        self.truncatesvd_data = pd.DataFrame(truncatesvd.fit_transform(self.data.T), index=self.data.T.index,
                                             columns=['X', 'Y'])
        return self.truncatesvd_data

    def plot(self, legend: bool = True, figsize: Tuple[int, int] = (10, 8),
             title: str = '', xlim: Tuple[float, float] = None, ylim: Tuple[float, float] = None,
             hidexticks: bool = False, save: bool = None) -> None:
        """
        Plots the reduced data (if 2D).

        Args:
            legend (bool, optional, default=True): If True, plots legend on the figure.
            figsize (Tuple[int, int], optional, default=10,8): Figure size: width, height in inches.
            title (str, optional, default=None): If not None, draws title string on the figure.
            xlim (Tuple[int, int], optional, default=None): Limits the values on the x-axis to the range (x_min, x_max).
            ylim (Tuple[int, int], optional, default=None): Limits the values on the y-axis to the range (y_min, y_max).
            hidexticks (bool, optional, default=False): If True, hides xticks.
            save (str, optional, default=None): Figure is not saved if save is None. <br/>  Set it with a output name if you want save it.
        """

        if self.truncatesvd_data.shape[1] != 2:
            raise Exception("data has too components. You can plot only bidimensional data.")

        colors = iter(cm.rainbow(np.linspace(0, 1, self.truncatesvd_data.shape[0])))
        fig, ax = plt.subplots(figsize=figsize)
        for i, u in enumerate(self.truncatesvd_data.index):
            ax.scatter(self.truncatesvd_data.loc[u].X, self.truncatesvd_data.loc[u].Y,
                       label=u, s=100, alpha=0.5, c=np.array([next(colors)]))

        # Put a legend to the right of the current axis
        if legend:
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])

        if not hidexticks:
            ax.set_xticks([])
            ax.set_yticks([])

        if not title is None:
            plt.title(title)

        if save:
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

        plt.close()
