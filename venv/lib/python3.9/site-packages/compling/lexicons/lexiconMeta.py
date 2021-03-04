import abc
from typing import *

class LexiconMeta(metaclass=abc.ABCMeta):
    """
    Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment _lexicon_
    to assign a polarity value to each text document by following a basic algorithm. A sentiment lexicon is a
    list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic
    orientation (i.e. polarity) as either _positive_ (pos), _negative_ (neg), _neutral_ (obj).
    """

    def __init__(self, pos: Iterable[str] = None) -> None:
        """
        Args:
            pos (Tuple[str], optional, default=None): Some lexicons provide a polarity of a token for each part of speech that token may have in the speech. <br/> If not None, only the polarities for the parts of speech in the pos tuple will be considered.
        """

        pos_dict = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}
        self.__PoS__ = [k for k, v in pos_dict.items() if pos is None or v in pos]

    @abc.abstractmethod
    def polarity(self, token:str) -> dict:
        """
        Returns the token polarities.

        Args:
            token (str): The text of the input token.

        Returns:
            dict: Polarities type as keys, sentiment values as values.

                    Example:
                    {
                     'pos' : 0.9,
                     'neg' : 0.1,
                     'obj' : 0.3
                    }
        """

    def polarities(self, bag_of_words: List[str]) -> dict:
        """
        Returns the polarities of the tokens in bag_of_words.

        Args:
            bag_of_words (List[str]): List of token.

        Returns:
            dict: Tokens as key, polarity dict as values.

                    Example:
                    {
                     token1: {
                                'pos' : 0.9,
                                'neg' : 0.1,
                                'obj' : 0.3
                              },
                     ...,
                     token2 : {...}
                     }
        """
        return {token: self.polarity(token) for token in bag_of_words}