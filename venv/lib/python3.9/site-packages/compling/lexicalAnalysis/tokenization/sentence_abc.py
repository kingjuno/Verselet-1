import abc
from typing import *

class Sentence(metaclass=abc.ABCMeta):
    """
    Represents a generic sentence, which is a sequence of tokens in the input.
    A sentence is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
    of tokens.
    """

    @abc.abstractmethod
    def named_entities(self) -> List[str]:
        """Returns named entities in the sentence."""

    @abc.abstractmethod
    def text(self) -> str:
        """Return the text of the sentence."""

    @abc.abstractmethod
    def lower(self) -> str:
        """Return the lowercase version of the sentence text."""

    @abc.abstractmethod
    def negations(self) -> str:
        """Return the text of the sentence where the text of negated tokens are preceded by the prefix 'NOT_'"""

    @abc.abstractmethod
    def lemma(self) -> str:
        """Returns a version of the sentence text with tokens replace by their lemma."""

    @abc.abstractmethod
    def stem(self) -> str:
        """Returns a version of the sentence text with tokens replace by their stem."""

    @abc.abstractmethod
    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the sentence."""

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Converts the sentence to a dict record."""

    @abc.abstractmethod
    def sentiment(self) -> Dict[str, float]:
        """
        Returns the sentence polarities. <br/>
        Each polarity value is between 0 and 1. They are calculated as the average of the tokens polarities greater than 0. <br/>
        _p_ in _[0,1]_

        Returns:
            Dict[str, float]: Polarities type as keys, sentiment values as values.

                    Example:
                    sentence.text = "damn your friend, I hate her"

                    >> sentence.sentiment()
                    {
                     'pos' : 0.125,
                     'neg' : 0.775,
                     'obj' : 0.100
                    }
        """