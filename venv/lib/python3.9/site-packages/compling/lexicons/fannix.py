import csv
import pkg_resources
from compling.descriptor import paramtypecheck
from compling.lexicons.lexiconMeta import LexiconMeta

csv.field_size_limit(1000000)

# --* path fannix file *--
__fannix__ = pkg_resources.resource_filename('compling', 'senti-lexicons/fannix.csv')


class Fannix(LexiconMeta):
    """
    Sentiment Lexicon for Chinese Language.

    https://github.com/fannix/Chinese-Sentiment-Lexicon/
    """

    def __init__(self) -> None:
        """
        **\_\_init\_\_**: Creates a new Fannix Lexicon object for Chinese Sentiment Analysis.
        """

        super().__init__()

        # lexicon object
        self.__sentiment__ = dict()

        # read from file
        with open(__fannix__, encoding='utf-8', mode='r') as f:
            rows = csv.reader(f, delimiter=',')

            columns = next(rows)

            for row in rows:
                record = dict(zip(columns, row))
                lemma = record['lemma'].lower()
                self.__sentiment__[lemma] = record

    def polarity(self, token: str) -> dict:
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence, neutral value are neutral valence.'

        Args:
            token (str): The input token.

        Returns:
            dict: A positive, a negative and a neutral value.
        """

        polarities = dict({'neg': 0.0, 'pos': 0.0, 'obj': 0.0})

        # text processing
        is_negated = True if token.startswith('NOT_') else False
        if is_negated:
            token = token.replace("NOT_", "")
        token = token.lower()

        # polarities not available
        if token not in self.__sentiment__:
            return polarities

        # polarities available
        sentiment = self.__sentiment__[token]
        pos, neg, obj = [float(sentiment[p]) for p in polarities.keys()]

        # Inversion of polarity
        if is_negated:
            pos, neg = neg, pos

        # Positive - Negative
        polarities['pos'] += pos
        polarities['neg'] += neg

        # Neutral
        polarities['obj'] += obj

        return polarities
