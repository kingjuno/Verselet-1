import abc
from typing import Dict

class Token(metaclass=abc.ABCMeta):
    """
    Represents a generic "token", which is a sequence of characters in the input.
    A token is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
    of tokens.
    """

    @abc.abstractmethod
    def sentiment(self) -> Dict[str, float]:
        """
        Returns the token polarities. <br/>
        Each polarity value is between 0 and 1. <br/>
        _p_ in _[0,1]_

        Returns:
            Dict[str, float]: Polarities type as keys, sentiment values as values.

                    Example:
                    token.text="fuck"

                    >> token.sentiment()
                    {
                     'pos' : 0.0,
                     'neg' : 1.0,
                     'obj' : 0.0
                    }
        """

    @abc.abstractmethod
    def text(self) -> str:
        """Returns the text of the token."""


    @abc.abstractmethod
    def shape(self) -> str:
        """
        Returns a transformed token version to show orthographic features of the token.

        Alphabetic characters are replaced by x or X, and numeric characters are replaced by d, and sequences of the
        same character are truncated after length 4. For example, "Xxxx" or "dd".
        """

    @abc.abstractmethod
    def lower(self) -> str:
        """Returns the lowercase version of the token text."""

    @abc.abstractmethod
    def stem(self) -> str:
        """Returns the stem of the token text."""

    @abc.abstractmethod
    def lemma(self) -> str:
        """Returns the lemma of the token text."""

    @abc.abstractmethod
    def pos(self) -> str:
        """Returns the pos tag of the token text."""

    @abc.abstractmethod
    def dep(self) -> str:
        """Returns the dep tag of the token text."""

    @abc.abstractmethod
    def lang(self) -> str:
        """Returns the language of the token."""

    @abc.abstractmethod
    def is_stopword(self) -> bool:
        """Returns True if the token text is a stopword else False."""

    @abc.abstractmethod
    def is_ngram(self) -> bool:
        """Returns True if the token text is a ngram else False."""

    @abc.abstractmethod
    def is_digit(self) -> bool:
        """Returns True if the token text is a digit else False."""

    @abc.abstractmethod
    def is_upper(self) -> bool:
        """Returns True if the token text is upper else False."""

    @abc.abstractmethod
    def is_capitalize(self) -> bool:
        """Returns True if the token text is capitalize else False."""

    @abc.abstractmethod
    def is_punct(self) -> bool:
        """Returns True if the token text is a punctuation symbol else False."""

    @abc.abstractmethod
    def is_space(self) -> bool:
        """Returns True if the token text is a space character else False."""

    @abc.abstractmethod
    def is_bracket(self) -> bool:
        """Returns True if the token text is a bracket symbol else False."""

    @abc.abstractmethod
    def is_ascii(self) -> bool:
        """Returns True if the token text is encoded in ascii else False."""

    @abc.abstractmethod
    def is_negated(self) -> bool:
        """Returns True if the token text is negated in the sentence."""

    @abc.abstractmethod
    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the token."""

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Converts the token object to a dict record."""
