from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from compling.sentiment.lexicon.lexicon import Lexicon


class Vader(Lexicon):
    """VADER Lexicon Implementation of Lexicon Abastract Class."""

    def __init__(self) -> None:
        """**\_\_init\_\_**: Creates a new Vader object."""
        self.vader = SentimentIntensityAnalyzer()

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

        polarities = self.vader.polarity_scores(token.replace("NOT_", ""))

        # polarity inversion
        if token.startswith('NOT_'):
            polarities['neg'], polarities['pos'] = polarities['pos'], polarities['neg']

        polarities['obj'] = polarities['neu']
        del polarities['neu']
        del polarities['compound']

        return polarities