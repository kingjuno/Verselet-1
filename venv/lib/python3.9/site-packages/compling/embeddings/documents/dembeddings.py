import abc
from compling.embeddings.embeddings import Embeddings
from typing import *


class DocumentEmbeddings(Embeddings, metaclass=abc.ABCMeta):
    """Document Embedding abstract class."""

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

        vectors = self.model.docvecs
        n = len(vectors)
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
        vectors = self.model.docvecs
        #print([tag for tag in self.model.docvecs.offset2doctag])
        return vectors.most_similar(positive=positive, negative=negative, topn=topn)

    def similarity(self, doc_id1: str, doc_id2: str) -> float:
        """
        Computes cosine similarity between two words/doc_ids.

        Args:
            id1 (str): First word/doc_id.
            id2 (str): First word/doc_id.

        Returns:
            float: Cosine similarity between two vectors.
        """

        vectors = self.model.docvecs
        return vectors.similarity(doc_id1, doc_id2)


    def run(self, vector_size:int=100, alpha:float=0.025, window:int=5, min_count:int=5, workers:int=3,
            min_alpha:int=0.001, epochs:int=25, dm:int=0) -> None:
        """
        Trains a Neural Network and builds a Word Embeddings Model.

        See: https://radimrehurek.com/gensim/models/doc2vec.html ."""

        super(DocumentEmbeddings, self).run(vector_size=vector_size, dm=dm, alpha=alpha,
                                            window=window, min_count=min_count,
                                        workers=workers, min_alpha=min_alpha, epochs=epochs)
