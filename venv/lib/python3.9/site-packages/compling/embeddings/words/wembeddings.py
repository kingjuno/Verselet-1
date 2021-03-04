import abc
from compling.embeddings.embeddings import Embeddings
from typing import *


class WordEmbeddings(Embeddings, metaclass=abc.ABCMeta):
    """Word Embedding abstract class."""

    def most_similar_threshold(self, positive: Union[list, str] = None,
                               negative: Union[list, str] = None,
                               threshold: float = 0.75) -> Dict[str, float]:
        """
        Finds the most similar vectors, whose cosine similarity is lower than threshold.
        Positive words/doc_ids contribute positively towards the similarity, negative words/doc_ids negatively.
        This method computes cosine similarity between a simple mean of the projection weight vectors of the
        given words/doc_ids and the vectors for each word/doc_id in the model.

        Args:
            positive (Union[list, str]): List of words/doc_ids that contribute positively.
            negative (Union[list, str]): List of words/doc_ids that contribute negatively.
            threshold (float, optional, default=0.75): Cosine similarity threshold.

        Returns:
            Dict[str, float]: Words/doc_ids as keys, cosine similarity values as values.
        """

        vectors = self.model.wv
        n = len(vectors.vocab)
        mst_res = {item[0]: item[1] for item in vectors.most_similar(positive=positive, negative=negative, topn=n)
                   if item[1] > threshold}
        return mst_res

    def most_similar(self, positive: Union[list, str] = None,
                     negative: Union[list, str] = None,
                     topn: int = 10) -> Dict[str, float]:
        """
        Finds the top-N most similar words/doc_ids.
        Positive words/doc_ids contribute positively towards the similarity, negative words/doc_ids negatively.
        This method computes cosine similarity between a simple mean of the projection weight vectors of the
        given words/doc_ids and the vectors for each word/doc_id in the model.

        Args:
            positive (Union[list, str]): List of words/doc_ids that contribute positively.
            negative (Union[list, str]): List of words/doc_ids that contribute negatively.
            topn (int, optional, default=10): Number of top-N similar words to return.

        Returns:
            Dict[str, float]: Words/doc_ids as keys, cosine similarity values as values.
        """
        vectors = self.model.wv
        return dict(vectors.most_similar(positive=positive, negative=negative, topn=topn))

    def similarity(self, word1: str, word2: str) -> float:
        """
        Computes cosine similarity between two words/doc_ids.

        Args:
            id1 (str): First word/doc_id.
            id2 (str): First word/doc_id.

        Returns:
            float: Cosine similarity between two vectors.
        """

        vectors = self.model.wv
        return vectors.similarity(word1, word2)

    def run(self, size=100, sg=0, alpha=0.025, window=5, min_count=5, workers=3,
            min_alpha=0.001, epochs=25) -> None:
        """
        Trains a Neural Network and builds a Word Embeddings Model.

        See: https://radimrehurek.com/gensim/models/word2vec.html ."""

        super(WordEmbeddings, self).run(size=size, sg=sg, alpha=alpha, window=window, min_count=min_count,
                                        workers=workers, min_alpha=min_alpha, epochs=epochs)
