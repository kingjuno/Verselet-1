import csv
import pkg_resources
from compling.sentiment.lexicon.lexicon import Lexicon
from collections import defaultdict
from typing import Tuple

csv.field_size_limit(1000000)

__sentix__ = pkg_resources.resource_filename('compling', 'senti-lexicons/sentix.csv')

class Sentix(Lexicon):
    """Sentix Lexicon Implementation of Lexicon Abastract Class.

    Italian Language.

    http://valeriobasile.github.io/twita/sentix.html
    """

    def __init__(self, pos: Tuple[str, str] = None) -> None:
        """
        **\_\_init\_\_**: Creates a new Sentiwordnet Italian object.

        Args:
            pos (Tuple[str], optional, default=None): SentiWordNet Lexicon returns a token polarities for each part of speech that token may have in the speech. <br/> If not None, filters the token polarities for part of speech in the pos tuple.

        This class sums the polarity value of the parts of speech you choose
        """

        self.sentiment = defaultdict(lambda: defaultdict(list))

        with open(__sentix__, encoding='utf-8', mode='r') as f:
            rows = csv.reader(f, delimiter='\t')

            columns = next(rows)

            for row in rows:
                record = dict(zip(columns, row))
                lemma, synset = record['lemma'].lower(), record['POS']
                self.sentiment[lemma][synset].append(record)

        pos_dict = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}
        self.pos = [k for k, v in pos_dict.items() if pos is None or v in pos or len(pos) == 0]

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

        for synset in self.sentiment[token.replace("NOT_", "").lower()]:
            if not synset in self.pos:
                continue

            for record in self.sentiment[token.replace("NOT_", "").lower()][synset]:

                polarity = float(record['polarity'])
                pos = 0 if polarity < 0 else polarity
                neg = 0 if polarity > 0 else -polarity
                obj = 1 - float(record['intensity'])


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

if __name__ == '__main__':
    s = Sentix()
    print(s.polarity('essere'))