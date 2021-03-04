import gensim
from compling.embeddings.words.wembeddings import WordEmbeddings
from typing import *


class Word2vec(WordEmbeddings):
    """
    Word2Vec is one of the most popular technique to learn word embeddings using shallow neural network. It was developed by Tomas Mikolov in 2013 at Google.

    It can be obtained using two methods (both involving Neural Networks): Skip Gram and Common Bag Of Words (CBOW)
    CBOW Model: This method takes the context of each word as the input and tries to predict the word corresponding to the context.

    Skip – gram follows the same topology as of CBOW. It just flips CBOW’s architecture on its head. The aim of skip-gram is to predict the context given a word.
    """
    def __init__(self, index: Iterable[dict]=None, output:str=None, text_field='text', skipgram_ws: int = None, processing:Callable=None):
        super().__init__(output=output, index=index, text_field=text_field, tag=False,
                         skipgram_ws=skipgram_ws, module=gensim.models.Word2Vec, processing=processing)
