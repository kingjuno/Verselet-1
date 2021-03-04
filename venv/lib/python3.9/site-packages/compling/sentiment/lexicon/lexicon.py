import abc
from typing import List


class Lexicon(metaclass=abc.ABCMeta):
    """
    Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment _lexicon_
     to assign a polarity value to each text document by following a basic algrithm. A sentiment lexicon is a
     list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic
     orientation (i.e. polarity) as either _positive_ or _negative_.
    """

    @abc.abstractmethod
    def polarity(self, token: str) -> dict:
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence, neutral value are neutral valence.'

        Args:
            token (str): The input token.

        Returns:
            dict: A positive, a negative and a neutral value
        """

    def polarities(self, bag_of_words: List[str]) -> dict:
        """
        Returns the polarities of the tokens in bag_of_words.

        Args:
            bag_of_words (List[str]): List of token.

        Returns:
            dict: A positive, a negative and a neutral value for each token
        """
        return {token: self.polarity(token) for token in bag_of_words}
