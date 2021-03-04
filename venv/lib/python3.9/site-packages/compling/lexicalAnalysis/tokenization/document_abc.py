import abc
from typing import *


class Document(metaclass=abc.ABCMeta):
    """
    Represents a generic document, which is a sequence of paragraph in the input.
    A document is identified by grouping a list of paragraph.
   """

    @abc.abstractmethod
    def sentiment(self) -> Dict[str, float]:
        """
        Returns the document polarities. <br/>
        Each polarity value is between 0 and 1. They are calculated as the average of the paragraphs polarities greater than 0. <br/>
        _p_ in _[0,1]_

        Returns:
            Dict[str, float]: Polarities type as keys, sentiment values as values.
        """

    @abc.abstractmethod
    def named_entities(self) -> List[str]:
        """Returns named entities in the document."""

    @abc.abstractmethod
    def text(self) -> str:
        """Returns the text of the document."""

    @abc.abstractmethod
    def lower(self) -> str:
        """Returns the lower of the document."""

    @abc.abstractmethod
    def lemma(self) -> str:
        """Returns a version of the document text with tokens replace by their lemma."""

    @abc.abstractmethod
    def negations(self) -> str:
        """Returns the text of the document where the text of negated tokens are preceded by the prefix 'NOT_'."""

    @abc.abstractmethod
    def stem(self) -> str:
        """Returns a version of the document text with tokens replace by their stem."""

    @abc.abstractmethod
    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the document."""

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Converts the document to a dict record."""