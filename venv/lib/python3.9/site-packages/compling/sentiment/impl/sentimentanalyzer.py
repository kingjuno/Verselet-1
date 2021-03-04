import re
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from compling.sentiment.sentiment import SentimentLexiconBased
from typing import *
from wordcloud import WordCloud


class SentimentAnalyzer(SentimentLexiconBased):
    """
    The most popular unsupervised strategies used in sentiment analysis are lexical-based methods. They make use of a predefined list of words, where each word is associated with a specific sentiment. Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment lexicon to assign a polarity value to each text document by following a basic algrithm. A sentiment lexicon is a list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic orientation (i.e. polarity) as either positive or negative.

    A SentimentAnalyzer object allows to perform sentiment analysis through a lexicon-based approach.

    SentimentAnalyzer uses a summation _strategy_: the polarity level of a document is calculated as the sum of the polarities of all the words making up the
    document.

    The analysis detects negation pattern and reverses the negated tokens polarity.

    Providing a regex, you can filter sentences/paragraphs/documents to analyze.

    Providing a pos list and/or a dep list you can filter the words whose polarities will be summed.
    """

    def filter(self, index: Iterable[dict],
               regex_pattern: str,
               text_field: str = 'text') -> Iterable[dict]:

        text_field+='_'
        pattern = re.compile(regex_pattern)

        self.__filtered_id__ = defaultdict(list)

        # Index filtered grouped by group_by_field
        for record in tqdm(index, desc='Filtering in progress...', leave=True, position=0):
            if pattern.match(record[text_field]):

                # add id to __filtered_id_
                for k in record:
                    if '_id_' in k:
                        self.__filtered_id__[k].append(record[k])
                        break

                yield record

    def run(self, index: Iterable[dict],
            text_field: str='text',
            min_len: int = 0,
            lang: str = None,
            pos: Tuple[str, ...] = None,
            dep: Tuple[str, ...] = None) -> Dict[str, Dict[str, float]]:

        # Info about sentiment
        polarities = defaultdict(lambda: defaultdict(float))
        count = defaultdict(lambda: defaultdict(int))

        text_field = text_field+'_'


        for record in tqdm(index, desc='SentimentAnalysis in progress...', leave=True, position=0):

            n_token = len(record[text_field].split())
            if n_token == 1 and len(record[text_field]) < min_len or min_len > n_token and n_token > 1:
                continue

            if lang is not None and lang != record['lang_'] or \
                    pos is not None and record['pos_'] in pos or \
                    dep is not None and record['dep_'] in dep:
                continue

            key = " + ".join([str(record[g]) for g in self.group_by_field])

            for k, v in record['sentiment_'].items():
                polarities[key][k] += v
                if v > 0:
                    count[key][k] += 1

        for k in polarities.keys():
            if count[k]['pos'] > 0 or count[k]['neg'] > 0:
                polarities[k]['pos'] /= max(count[k]['pos'], count[k]['neg'])
                polarities[k]['neg'] /= max(count[k]['pos'], count[k]['neg'])
            if count[k]['obj'] > 0 or count[k]['obj'] > 0:
                polarities[k]['obj'] /= count[k]['obj']


        return polarities

    def sentitokens(self,
                    tokens: Iterable[dict],
                    text_field:str='text',
                    min_len:int=0,
                    lang:str=None,
                    pos: Tuple[str, ...] = None,
                    dep: Tuple[str, ...] = None) -> dict:

        # Info about sentiment
        polarities = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        text_field = text_field + '_'

        if hasattr(self, '__filtered_id__'):
            key_id_filtered = list(self.__filtered_id__.keys())[0]
        else:
            key_id_filtered = None

        for record in tqdm(tokens, desc='Sentitokens classification in progress...', leave=True, position=0):

            if len(record[text_field]) < min_len:
                continue

            if lang is not None and lang!=record['lang_'] or\
                pos is not None and record['pos_'] in pos or \
                dep is not None and record['dep_'] in dep or \
                    key_id_filtered is not None and record[key_id_filtered] not in self.__filtered_id__[key_id_filtered]:
                continue

            key = " + ".join([str(record[g]) for g in self.group_by_field])

            if 'is_negated_' in record and record['is_negated_']:
                token = 'NOT_'+record[text_field]
            else:
                token = record[text_field]

            if record['sentiment_']['pos'] > record['sentiment_']['neg']:
                polarities[key]['pos'][token] += 1
            elif record['sentiment_']['neg'] > record['sentiment_']['pos']:
                polarities[key]['neg'][token] += 1

        return polarities

    def plot(self, polarities, ylabel: str = None, xlabel: str = None, figsize: Tuple[int, int] = (12, 8),
             title: str = None, hidexticks: bool = True, save: bool = None) -> None:
        """
        Draws a scatter plot of positive and negative polarities level for each group_by_field sort by time (If date_field is not None).

        Args:
            xlabel (str, optional, default=None): Label on x-axis.
            ylabel (str, optional, default=None): Label on y-axis.
            figsize (Tuple[int, int], optional, default=12,8): Figure size: width, height in inches.
            title (str, optional, default=None): If not None, draws title string on the figure.
            hidexticks (bool, optional, default=False): If True, hides xticks.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with an output name if you want save it.
        """

        plt.figure(figsize=figsize)
        plt.plot()

        polarities_ = {"pos": {"color": "red", "label": "Positive (+)"},
                      "neg": {"color": "black", "label": "Negative (-)"}}

        for polarity in polarities_:
            plt.tight_layout()
            x, y = list(polarities.keys()), [polarities[id_vector][polarity] for id_vector in polarities]
            plt.plot(x, y, label=polarities_[polarity]["label"], color=polarities_[polarity]["color"])
            plt.xticks(x, rotation="vertical")
            plt.title('\n{}'.format(title), size=20)
            if not ylabel is None:
                plt.ylabel('{}\n'.format(ylabel), size=20)
            if not xlabel is None:
                plt.xlabel('\n{}'.format(xlabel), size=20)

        plt.legend()  # bbox_to_anchor=(1.5, 0.5), loc='right', ncol=1)

        if not hidexticks:
            plt.xticks([])

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

    def circleplot(self, polarities:Dict[str, Dict[str, float]], radius: int = 3, figsize: Tuple[int, int] = (10, 10), title: str = None,
                   width_modifier: float = 1.3,
                   offset: float = 0.8, save: bool = False) -> None:
        """
        Draws a circle plot of positive and negative polarities level for each group_by_field sort by time (If date_field is not None).

        Args:
            polarities (Dict[str, Dict[str, float]]): The result of the method run.
            radius (int, optional, default=3): The radius of the circle.
            figsize (Tuple[int, int], optional, default=10,10): Figure size: width, height in inches.
            width_modifier (float, optional, default=1.3): Width of the bars.
            offset (float, optional, default=0.8): Offset for the label on the bars.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with an output name if you want save it.
            title (str, optional, default=None):  If not None, draws title string on the figure.
        """

        data = polarities

        plt.figure(figsize=figsize)
        ax = plt.subplot(111, polar=True)
        ax.axis('off')

        N = len(data)
        radius = radius

        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = (width_modifier * np.pi) / N

        pos_values, neg_values = np.array([data[i]["pos"] for i in data]), np.array([data[i]["neg"] for i in data])

        pos = ax.bar(theta, pos_values, width=width, bottom=radius)
        neg = ax.bar(theta, -neg_values, width=width, bottom=radius)

        for p, n in zip(pos, neg):
            p.set_facecolor("red")
            p.set_alpha(0.8)
            n.set_facecolor("black")
            n.set_alpha(0.8)

        # labeling
        for i, bar in enumerate(pos):
            t = theta[i] + 0.002
            x, y = (bar.get_x() + width / 2, offset * len(list(data)[i]) + bar.get_height())
            if np.cos(t) < 0: t = t - np.pi
            ax.text(x, y, list(data)[i], rotation=np.rad2deg(t), ha="center", va="center")

        if title:
            plt.title(title)

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

    def wordcloud(self, words:Dict[str, Dict[str, int]],
                  color: str = 'black', title: str = None, figsize: Tuple[int, int] = (10, 8),
                  save=None, width: int = 1000, height: int = 1000,
                  max_words: int = 100) -> None:
        """
        Draws a word Cloud with the words of grouped_by_field_value.

        Args:
            words (Dict[str, Dict[str, float]]): The sentitokens for a specific key and a specific polarity ['pos'/'neg'].
            color (str, optional, default=black): Background color.
            title (str, optional, default=None): If not None, draws title string on the figure.
            figsize (Tuple[int, int], optional, default=10,10): Figure size: width, height in inches.
            save (str, optional, default=None): Figure is not saved if save is None. Set it with a output name if you want save it.
            width (int, optional, default=1000): Width of the canvas.
            height (int, optional, default=1000): Height of the canvas.
            max_words (int, optional, default=100): The maximum number of words.
        """



        sentiment = words
        wordcloud = WordCloud(width=width, background_color=color, height=height,
                              max_words=max_words).generate_from_frequencies(sentiment)
        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, label=title)
        plt.title(title, fontsize=22)

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

        plt.close()
