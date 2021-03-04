import abc
import compling.nlp
from typing import *


class Tokenization(metaclass=abc.ABCMeta):
    """
    Tokenization converts input text to streams of tokens, where each token is a separate word, punctuation sign,
    number/amount, date, etc.
    """

    def __init__(self) -> None:

        # natural language processing object
        self.nlp = compling.nlp.NLP()

        self.text_key = self.nlp.config.get(s='Corpus', k='text_key')
        self.date_format = self.nlp.config.get(s='Corpus', k='date_format')

    @abc.abstractmethod
    def ngrams2tokens(self,
                      n: Union[int, Iterable[int]],
                      docs_in: Iterable[Dict[str, str]],
                      docs_out: Iterable[Dict[str, str]],
                      pos: Tuple[str, ...] = ("PROPN", "VERB", "NOUN", "ADJ"),
                      corpus_threshold: int = 50,
                      doc_threshold: int = 0,
                      len_gram: int = 3,
                      include: Tuple[str, ...] = None,
                      replace: bool = True) -> Iterable[Dict[int, str]]:
        """
        Calculates frequent n-grams in the corpus. They will be considered as unique tokens during the Tokenization task. <br/>
        Frequent n-grams will be calculated based on the documents in the input stream (docs_in). <br/>
        Frequent n-grams will be considered as unique tokens in the output stream documents (docs_out).

        Args:
           docs_in (Iterable[Dict[str, str]]): Stream of input json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Frequent n-grams will be calculated by scrolling this stream.
           docs_out (Iterable[Dict[str, str]]): Stream of output json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Frequent n-grams will be considered as unique tokens for each document in the stream. Each document will be yielded as output of this function.
           n (Union[int, Iterable[int]]): If int, the size of n-grams. (e.g. n=2, bigrams) <br/> If Iterable[int], the sizes of n-grams. (e.g. n=[2,3,5], bigrams, trigrams, fivegrams)
           pos (Tuple[str, ...], optional): default ('PROPN', 'VERB', 'NOUN', 'ADJ'). <br/> Part of speech of the first and the last token that make up n-grams. <br/> Filters the most informative n-grams. <br/> If None, the filter will be ignored.
           corpus_threshold (int, optional, default=50): Filters n-grams that have a corpus frequency greater than corpus_threshold.
           doc_threshold (int, optional, default=0): Filters n-grams that have frequency greater than doc_threshold. <br/> The frequency of an n-gram in the corpus is the sum of the frequency of that n-gram in documents where the ngram occurs at least doc_thresold times.
           len_gram (int, optional, default=3): The size of the first and the last token that make up n-grams must be at least 'len_gram'.
           include (Tuple[str, ...], optional, default=None): Include a list of arbitrary n-grams.
           replace (bool, optional, default=True): If True, replaces a n-gram with its tokens separated by '_'. <br/> Else, concatenates a new token, made merging the n-gram tokens with '_', to the n-gram.

        Returns:
            Iterable[Dict[str, str]]: Stream of json documents (docs_out) with frequent n-grams considered as unique token.
        """

    @abc.abstractmethod
    def run(self,
            docs: Iterable[Dict[str, str]],
            doc_id: int = 0,
            token_id: int = 0,
            sent_id: int = 0,
            para_id: int = 0,
            para_size: int = 3,
            index_doc: bool = True,
            index_sent: bool = True,
            index_para: bool = True) -> Iterable[Dict[str, dict]]:
        """
        Runs the tokenization for each document of the corpus.

        Args:
            docs (Iterable[Dict[str, str]]): Stream of json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Each document will be tokenized.
            doc_id (int, optional, default=0): Unique document identifier. <br/> Numeric id of documents. <br/> A progressive id will be assigned to the documents starting from this number.
            token_id (int, optional, default=0): Unique token identifier. <br/> Numeric id of tokens. <br/> A progressive id will be assigned to the tokens starting from this number.
            sent_id (int, optional, default=0): Unique sentence identifier. <br/> Numeric id of sentences. <br/> A progressive id will be assigned to the sentences starting from this number.
            para_id (int, optional, default=0): Unique paragraph identifier. <br/> Numeric id of paragraphs. <br/> A progressive id will be assigned to the paragraphs starting from this number.
            para_size (int, optional, default=3): The paragraph size: the number of sentences that makes up a paragraph.
            index_doc (bool, optional, default=True): If True, returns the records of the documents index as values of the key 'documents'.
            index_sent (bool, optional, default=True): If True, returns the records of the sentences index as values of the key 'sentences'.
            index_para (bool, optional, default=True): If True, returns the records of the paragraphs index as values of the key 'paragraphs'.

        Returns:
            Iterable[Dict[str, dict]]: Stream of tokens, sentences, paragraphs, documents records.
        """
