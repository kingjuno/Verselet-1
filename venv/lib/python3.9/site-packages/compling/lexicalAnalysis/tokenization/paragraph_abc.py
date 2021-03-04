import abc
from typing import *


class Paragraph(metaclass=abc.ABCMeta):
    """
    Represents a generic paragraph, which is a sequence of sentence in the input.
    A paragraph is identified by grouping a list of sentence.
    """

    @abc.abstractmethod
    def named_entities(self) -> List[str]:
        """Returns named entities in the paragraph."""

    @abc.abstractmethod
    def text(self) -> str:
        """Return the text of the paragraph."""

    @abc.abstractmethod
    def lower(self) -> str:
        """Return the lowercase text of the paragraph."""

    @abc.abstractmethod
    def lemma(self) -> str:
        """Returns a version of the paragraph text with tokens replace by their lemma."""

    @abc.abstractmethod
    def negations(self) -> str:
        """Return the text of the paragraph where the text of negated tokens are preceded by the prefix 'NOT_'."""

    @abc.abstractmethod
    def stem(self) -> str:
        """Returns a version of the paragraph text with tokens replace by their stem."""

    @abc.abstractmethod
    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the paragraph."""

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Converts the paragraph to a dict record."""

    def sentiment(self) -> Dict[str, float]:
        """
        Returns the paragraph polarities. <br/>
        Each polarity value is between 0 and 1. They are calculated as the average of the sentences polarities greater than 0. <br/>
        _p_ in _[0,1]_

        Returns:
            Dict[str, float]: Polarities type as keys, sentiment values as values.
        """