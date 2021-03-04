from compling.lexicons.lexiconMeta import LexiconMeta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Vader(LexiconMeta):
    """VADER Lexicon for English Language."""

    def __init__(self) -> None:

        super().__init__()
        self.__sentiment__ = SentimentIntensityAnalyzer()

    def polarity(self, token: str) -> dict:
        """
        Returns a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence, neutral value are neutral valence.'

        Args:
            token (str): The input token.

        Returns:
            dict: A positive, a negative and a neutral value.
        """

        # text processing
        is_negated = True if token.startswith('NOT_') else False
        if is_negated:
            token = token.replace("NOT_", "")
        token = token.lower()

        polarities = self.__sentiment__.polarity_scores(token)

        # polarity inversion
        if is_negated:
            polarities['neg'], polarities['pos'] = polarities['pos'], polarities['neg']

        polarities['obj'] = polarities['neu']
        del polarities['neu']
        del polarities['compound']

        return polarities