import csv
import pkg_resources
from compling.sentiment.lexicon.lexicon import Lexicon

csv.field_size_limit(1000000)

__fannix__ = pkg_resources.resource_filename('compling', 'senti-lexicons/fannix.csv')

class Fannix(Lexicon):
    """Sentix Lexicon Implementation of Lexicon Abastract Class.

    Chinese Language.

    https://github.com/fannix/Chinese-Sentiment-Lexicon/
    """

    def __init__(self) -> None:
        """
        **\_\_init\_\_**: Creates a new Sentiwordnet Chinese object.
        """

        self.sentiment = dict()

        with open(__fannix__, encoding='utf-8', mode='r') as f:
            rows = csv.reader(f, delimiter=',')

            columns = next(rows)

            for row in rows:
                record = dict(zip(columns, row))
                lemma = record['lemma'].lower()
                self.sentiment[lemma] = record


    def polarity(self, token: str) -> dict:
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

        polarities = dict({'neg': 0.0, 'pos': 0.0, 'obj': 0.0})
        count = dict({'neg': 0, 'pos': 0, 'obj': 0})

        if token.replace("NOT_", "").lower() not in self.sentiment:
            return polarities

        sentiment = self.sentiment[token.replace("NOT_", "").lower()]

        pos = float(sentiment['pos'])
        neg = float(sentiment['neg'])
        obj = float(sentiment['obj'])

        if token.startswith('NOT_'):

            if neg > 0:
                count['pos'] += 1
            if pos > 0:
                count['neg'] += 1

            polarities['neg'] += pos
            polarities['pos'] += neg
        else:

            if pos > 0:
                count['pos'] += 1
            if neg > 0:
                count['neg'] += 1

            polarities['pos'] += pos
            polarities['neg'] += neg

        if obj > 0:
            count['obj'] +=1

        polarities['obj'] += obj

        for k in polarities.keys():
            if count[k] > 0:
                if k in ("pos", "neg"):
                    polarities[k] /= max(count["pos"], count["neg"])
                else:
                    polarities[k] /= count[k]

        return polarities
