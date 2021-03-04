import abc
from typing import *


class SentimentLexiconBased(metaclass=abc.ABCMeta):
    """
    The most popular unsupervised strategies used in _sentiment analysis_ are _lexical-based_ methods. <br/>
    They make use of a predefined list of words, where each word is associated with a specific _sentiment_. <br/>
    Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment _lexicon_
     to assign a polarity value to each text document by following a basic algrithm. A sentiment lexicon is a
     list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic
     orientation (i.e. polarity) as either _positive_ or _negative_.
    """

    def __init__(self, group_by_field: Union[str, List[str]], date_field: str = None) -> None:
        """
        **\_\_init\_\_**: Creates a new SentimentAnalyzer object.

        Args:
            group_by_field (Union[str, List[str]]): Sentiments values are calculated for each different tuple of values. Tuples are defined by grouping records by fields in group_by_field.
            date_field (str, optional, default=None): If not None, Sentiment vectors are sorted by this field.

        """
        if isinstance(group_by_field, str):
            self.group_by_field = [group_by_field + '_']
        else:
            self.group_by_field = [g + '_' for g in group_by_field]

        self.group_by_field_key = " + ".join(self.group_by_field)

        self.date_field = date_field if date_field is None else date_field + '_'

    @abc.abstractmethod
    def filter(self, index: Iterable[dict],
               regex_pattern: str,
               text_field: str = 'text') -> Iterable[dict]:
        """
        Filters the tokens/sentences/paragraphs/documents to be considered to calculate a sentiment value.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            regex_pattern (str): The filter uses this regex.
            text_field (str, optional, default=text): For each record the regex will be evaluated on this field.
        Returns:
            Iterable[dict]: The record filtered.
        """

    @abc.abstractmethod
    def run(self, index: Iterable[dict],
            text_field: str = 'text',
            min_len: int = 0,
            lang: str = None,
            pos: Tuple[str, ...] = None,
            dep: Tuple[str, ...] = None) -> Dict[str, Dict[str, float]]:
        """
        Performs sentiment analysis of the texts in the index calculating the polarity level for each different
        group_by_field value.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >> s = SentimentAnalyzer(group_by_field='author')
                    >> sentences_filtered = s.filtered(sentences, regex_pattern='.*family.*')
                    >> s.run(index=sentences_filtered)

            text_field (str, optional, default=text): For each record 'min_len' will be checked on this field.
            min_len (int, optional, default=0): The minimum length a text must have to be considered
            lang (str, optional, default=None): You can filter the sentiment analysis for the document of a specific language.
            pos (Tuple[str, ...], optional, default=None): If index records are tokens, part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): If index records are tokens, dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.

        Returns:
            Dict[str, Dict[str, float]]: A dict contains the polarity value for each different grouped_by_field value.

                         Example:
                         {
                          "grouped_by_field1": {
                                                "pos": 0,
                                                "neg":1,
                                                "obj":3},
                           ...,
                         }
        """

    @abc.abstractmethod
    def sentitokens(self,
                    tokens: Iterable[dict],
                    text_field: str = 'text',
                    min_len: int = 0,
                    lang: str = None,
                    pos: Tuple[str, ...] = None,
                    dep: Tuple[str, ...] = None) -> dict:
        """

        Args:
            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.
            text_field (str, optional, default=text): The text field of each token.
            min_len (int, optional, default=0): The minimum length a token must have to be considered
            lang (str, optional, default=None): You can filter the token of a specific language.
            pos (Tuple[str, ...], optional, default=None): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.

        Returns:
            dict: A dict containing the words classified as positive/negative, as keys, with their frequency value, as values, for each
            different grouped_by_field value.

                         Example:
                         {
                          "grouped_by_field1": {
                                                "neg": {
                                                        "fuck": 12,
                                                        "bad": 7,
                                                        ...
                                                        },
                                                "pos": {
                                                        "good": 11,
                                                        "love": 2,
                                                        ...
                                                        }
                                                },
                          ...
                        }
        """