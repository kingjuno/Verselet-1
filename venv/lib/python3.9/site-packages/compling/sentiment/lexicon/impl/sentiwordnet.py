from nltk.corpus import sentiwordnet as swn
from compling.sentiment.lexicon.lexicon import Lexicon
from typing import Tuple

class Sentiwordnet(Lexicon):
    """Sentiwordnet Lexicon Implementation of Lexicon Abastract Class."""

    def __init__(self, pos: Tuple[str, str] = None) -> None:
        """
        **\_\_init\_\_**: Creates a new Sentiwordnet object.

        Args:
            pos (Tuple[str], optional, default=None): SentiWordNet Lexicon returns a token polarities for each part of speech that token may have in the speech. <br/> If not None, filters the token polarities for part of speech in the pos tuple.

        This class sums the polarity value of the parts of speech you choose
        """

        pos_dict = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}
        self.pos = [k for k, v in pos_dict.items() if pos is None or v in pos or len(pos) == 0]

    def polarity(self, token: str) -> dict:
        """
        Returns the token polarities.

        Args:
            token (str): The text of the input token.

        Args:
            dict: Polarities type as keys, sentiment values as values.

                    Example:
                    {
                     'pos' : 0.9,
                     'neg' : 0.1,
                     'obj' : 0.3
                    }
        """

        senti_synsets = [senti_synset for senti_synset in list(swn.senti_synsets(token.replace("NOT_", "")))
                 if senti_synset.synset._pos in self.pos]

        polarities = dict({'neg': 0.0, 'pos': 0.0, 'obj': 0.0})
        count = dict({'neg': 0, 'pos': 0, 'obj': 0})

        for senti_synset in senti_synsets:
            pos = senti_synset.pos_score()
            neg = senti_synset.neg_score()
            obj = senti_synset.obj_score()

            if token.startswith('NOT_'):

                if pos > 0:
                    count['neg'] += 1
                if neg > 0:
                    count['pos'] += 1

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
                count['obj'] += 1
            polarities['obj'] += obj

        for p in ['pos', 'neg', 'obj']:
            if count[p] > 0:
                if p in ("pos", "neg"):
                    polarities[p] /= max(count["pos"], count["neg"])
                else:
                    polarities[p] /= count[p]

        return polarities

