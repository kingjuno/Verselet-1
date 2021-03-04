import abc
from compling.nlp import NLP
import gensim
from typing import *


class Embeddings(metaclass=abc.ABCMeta):
    """
    A word embedding is a learned representation for text where words that have the same meaning have a similar representation.

    Word embeddings are a class of techniques where individual words are represented as real-valued vectors in a predefined vector space. Each word is mapped to one vector and the vector values are learned in a way that resembles a neural network, and hence the technique is often lumped into the field of deep learning.

    Key to the approach is the idea of using a dense distributed representation for each word.

    Each word is represented by a real-valued vector, often tens or hundreds of dimensions. This is contrasted to the thousands or millions of dimensions required for sparse word representations, such as a one-hot encoding.
    """

    def __init__(self, index: Iterable[dict], module: gensim.models, output:str=None, text_field='text',
                 skipgram_ws: int = None, tag=False, id_field:Union[str, List[str]]=None, processing:Callable=None) -> None:
        """
        **\_\_init\_\_**: Creates a new Embeddings instance.

        Args:
           index (Iterable[dict]): Records of an index produced by tokenization.
           module (gensim.models): Gensim module.

                   Valid input:
                   - gensim.models.Word2Vec;
                   - gensim.models.fasttext.FastText;
                   - gensim.models.doc2vec.Doc2Vec

           output (str, optional, default=None): If not None, stores the model with the name in output.
           text_field (str, optional, default=text): The text field of the records.
           skipgram_ws (int, optional, default=None): If not None, text inside records was skipgram_splitted with skipgram_ws=skipgram_ws. <br/> Window size: size of sampling windows. <br/> The window of a word _w_i_ will be _[i-window_size, i+window_size+1]_ <br/> See: nlp.NLP.split_skipgram
           tag (bool, optional, default=True): If True, Tag each record with its id_field.
           id_field (Union[str, List[str]], optional, default=None): Id fields conteining tag for each records.
        """

        if id_field is not None:
            if isinstance(id_field, str):
                id_field = [id_field]

            id_field = " + ".join([i+'_' for i in id_field])

        self.id_field = id_field

        text_field += '_'

        # natural language processing object
        self.nlp = NLP()

        self.module = module
        self.model = None
        self.output = output

        if index is None:
            return

        def process(text):
            if processing is None: return text
            return processing(text)

        if tag:
            self.data = [gensim.models.doc2vec.TaggedDocument(words=process(record[text_field]).split(),
                                                              tags=[str(record[self.id_field])])
                         if not skipgram_ws else
                         gensim.models.doc2vec.TaggedDocument(
                             words=self.self.nlp.split_skipgram(process(record[text_field]), ws=skipgram_ws),
                             tags=[str(record[self.id_field])])
                         for record in index]

        else:
            self.data = [process(record[text_field]).split() if not skipgram_ws else
                         self.nlp.split_skipgram(process(record[text_field]), ws=skipgram_ws)
                         for record in index]

    def __getattr__(self, name):
        value = super(Embeddings, self).__getattr__(self, name)
        if name == 'model' and value is None:
            return self.load()
        else:
            return value

    def load(self, path):
        """Load a previously saved Embeddings model from file."""

        self.model = self.module.load(path)
        return self.model

    def save(self):
        """Stores the model. This saved model can be loaded again using load(), which supports
        getting vectors for vocabulary words."""

        self.model.save(self.output)

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
    def similarity(self, id1: str, id2: str) -> float:
        """
        Computes cosine similarity between two words/doc_ids.

        Args:
            id1 (str): First word/doc_id.
            id2 (str): First word/doc_id.

        Returns:
            float: Cosine similarity between two vectors.
        """

    def analogy(self, positive: List[str], negative: List[str], topn=10) -> Dict[str, float]:
        """
        Inferes an analogy.
        This method is the same of most_similar but forces to have positive and negative List[str] as input.

            Example:
            >> analogy(positive=[king, woman], negative=[man]) -> {queen: 0.99, ...}

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
        return self.most_similar(positive, negative, topn)

    def run(self, **kwargs) -> None:
        """Trains a Neural Network and builds a Embeddings Model."""

        param_dict = {k: v for k, v in locals()['kwargs'].items() if k not in ('self', 'epochs') and v is not None}
        model = self.module(**param_dict)

        model.build_vocab(self.data)

        model.train(self.data,
                    epochs=locals()['kwargs']['epochs'],
                    total_examples=model.corpus_count,
                    total_words=model.corpus_total_words)
        self.model = model

        if self.output is not None:
            self.save()
