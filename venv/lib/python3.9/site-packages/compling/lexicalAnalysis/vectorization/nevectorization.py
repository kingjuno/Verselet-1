import abc
from typing import *


class NEVectorization(metaclass=abc.ABCMeta):
    """
    The process of converting text into vector is called vectorization.
    The set of corpus documents vectorized corpus makes up the Vector Space Model, which can have a sparse or
    dense representation.

    A NEVectorization object allows you to create vectors grouping named_entities for arbitrary fields.

    Grouping named_entities by:

       * _doc_id_: you 're creating document vectors;
       * _sent_id_: you 're creating sentence vectors;
       * _author_: you're creating author vectors (each named_entities must have an 'author' field);
       ...

    You can group by multiple fields.

    It offers several functions to set the vector components values, such as:

       * **One-hot encoding** (binary values 0/1);
       * **Tf** (Term Frequency);
       * **TfIdf** (Term Frequency Inverse Document Frequency);
       * **MI** (Mutual Information)

    You can specify the vectorization representation format: Term x Document matrix, Postings list.
    """

    def __init__(self, group_by_field: Union[str, List[str]], ne_field: str = 'named_entities') -> None:
        """
        Args:
            group_by_field (Union[str, List[str]]): Fields linked to named_entities in the corpus (e.g. doc_id, sent_id, metadata1, ...).  <br/> The named_entities will be grouped by these field.
            ne_field (str, optional, default=named_entities): A field containing the named_entities list.
        """

        self.ne_field = ne_field + '_'

        if isinstance(group_by_field, str):
            self.group_by_field = [group_by_field + '_']
        else:
            self.group_by_field = [g + '_' for g in group_by_field]

        self.group_by_field_key = " + ".join(self.group_by_field)

    @abc.abstractmethod
    def tf(self, index: Iterable[dict],
           min_len: int = 0,
           min_count: int = 0,
           format_: str = "docterm-matrix",
           boolean=False) -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

            boolean (bool, optional, default=False): If True return Boolean Vectors else Term Frequency. <br/> If True, the result is the same as onehot method.

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.
        """

    @abc.abstractmethod
    def tfidf(self,
              index: Iterable[dict],
              normalize=True,
              min_len=0,
              min_count: int = 0,
              format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency Inverse Document Frequency.


        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            normalize (bool, optional, default=True): If True, normalizes TF for max(TF).
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.
        """

    @abc.abstractmethod
    def mi(self,
           index: Iterable[dict],
           min_len: int = 0,
           min_count: int = 0,
           format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterator[dict]]:
        """
        Calculates Mutual Information.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.
        """


    @abc.abstractmethod
    def onehot(self, index: Iterable[dict], min_len: int = 0,
               min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates One-hot encoding.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
             min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.
        """

    @abc.abstractmethod
    def run(self,
            mode: str,
            index: Iterable[dict],
            normalize=True,
            min_len=0,
            min_count=0,
            metadata: Dict[str, dict] = None) -> Iterable[dict]:
        """
        Runs the vectorization grouping named_entities by self.ne_field and self.group_by_field.

        Args:
            mode (str): Vectorization mode. <br/>

                    Valid input values:
                    ["tf", "tfidf", "mi", "onehot"]

            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            normalize (bool, optional, default=True): If True, normalizes TF for max(TF). <br/> This parameter is ignored if mode in ['tf', 'onehot', 'mi'].
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            metadata (Dict[str, dict], optional, default=None): A dict containing metadata for each different group_by_field value.  <br/> Each vector will be associated with its own metadata.

        Returns:
            Iterable[dict]: Returns a docterm matrix.
        """
