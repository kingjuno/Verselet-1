from nltk.corpus import sentiwordnet as swn
from compling.lexicons.lexiconMeta import LexiconMeta


class Sentiwordnet(LexiconMeta):
    """Sentiwordnet Lexicon for English Language."""

    def __init__(self):
        module = __import__('compling.languages.english')
        language = getattr(getattr(module, 'languages'), 'english')
        super().__init__(language.pos_token_sentiment)

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

        senti_synsets = [senti_synset for senti_synset in
                         list(swn.senti_synsets(token))
                         if senti_synset.synset._pos in self.__PoS__]

        polarities = dict({'neg': 0.0, 'pos': 0.0, 'obj': 0.0})
        count = dict({'neg': 0, 'pos': 0, 'obj': 0})

        for senti_synset in senti_synsets:
            pos = senti_synset.pos_score()
            neg = senti_synset.neg_score()
            obj = senti_synset.obj_score()

            # Inversion of polarity
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
