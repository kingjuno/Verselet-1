import csv
import pkg_resources
from collections import defaultdict
from compling.languages import italian
from compling.lexicons.lexiconMeta import LexiconMeta

csv.field_size_limit(1000000)

# Path to Sentix Lexicon: csv file
__sentix__ = pkg_resources.resource_filename('compling', 'senti-lexicons/sentix.csv')

# Parts of speech of the token we want to analyze
__pos__ = italian.pos_token_sentiment


class Sentix(LexiconMeta):
    """
    Sentiment Lexicon for Italian Language.

    http://valeriobasile.github.io/twita/sentix.html
    """

    def __init__(self):

        module = __import__('compling.languages.italian')
        language = getattr(getattr(module, 'languages'), 'italian')
        super().__init__(language.pos_token_sentiment)

        # lexicon object
        self.__sentiment__ = defaultdict(lambda: defaultdict(list))

        # read from file
        with open(__sentix__, encoding='utf-8', mode='r') as f:
            rows = csv.reader(f, delimiter='\t')

            columns = next(rows)

            for row in rows:
                record = dict(zip(columns, row))
                lemma, synset = record['lemma'].lower(), record['POS']
                self.__sentiment__[lemma][synset].append(record)

    def polarity(self, token: str) -> dict:
        """
        Returns a float for sentiment strength based on the input text.

        * The positive polarity of a token is calculated as the average of the positive polarities of its synsets that have a positive or negative polarity greater than 0.
        * The negative polarity of a token is calculated as the average of the positive polarities of its synsets that have a positive polarity or negative greater than 0.
        * The neutral polarity of a token is calculated as the average of the positive polarities of its synsets that have a neutral polarity greater than 0.

        Args:
            token (str): The text of the input token.

        Returns:
            dict: A positive, a negative and a neutral value.
        """

        # text processing
        is_negated = True if token.startswith('NOT_') else False
        if is_negated:
            token = token.replace("NOT_", "")
        token = token.lower()

        polarities = dict({'neg': 0.0, 'pos': 0.0, 'obj': 0.0})
        count = dict({'neg': 0, 'pos': 0, 'obj': 0})

        if token not in self.__sentiment__:
            return polarities

        for synset in self.__sentiment__[token]:
            if synset not in self.__PoS__:
                continue

            for record in self.__sentiment__[token][synset]:

                polarity = float(record['polarity'])
                pos = 0 if polarity < 0 else polarity
                neg = 0 if polarity > 0 else -polarity
                obj = 1 - float(record['intensity'])

                if is_negated:
                    pos, neg = neg, pos

                if pos > 0:
                    count['pos'] += 1
                if neg > 0:
                    count['neg'] += 1

                polarities['pos'] += pos
                polarities['neg'] += neg

                if obj > 0:
                    count['obj'] += 1

                polarities['obj'] += obj

        # Normalization
        if count['pos'] > 0 or count['neg'] > 0:
            polarities['pos'] /= max(count["pos"], count["neg"])
            polarities['neg'] /= max(count["pos"], count["neg"])
        if count['obj'] > 0:
            polarities['obj'] /= count['obj']

        return polarities