import gensim
from compling.embeddings.words.wembeddings import WordEmbeddings
from typing import *


class Fasttext(WordEmbeddings):
    """
    FastText is able to achieve really good performance for word representations and sentence classification, specially in the case of rare words by making use of character level information.

    Each word is represented as a bag of character n-grams in addition to the word itself. This helps preserve the meaning of shorter words that may show up as ngrams of other words. Inherently, this also allows you to capture meaning for suffixes/prefixes.
    """
    def __init__(self, index: Iterable[dict]=None, output:str=None, text_field='text', skipgram_ws: int = None, processing:Callable=None):

        super().__init__(output=output, index=index, text_field=text_field, tag=False, skipgram_ws=skipgram_ws,
                         module=gensim.models.fasttext.FastText, processing=processing)