language = 'italian'
iso639 = 'it'

spacy_model_sm = iso639 + '_core_news_sm'
spacy_model_md = iso639 + '_core_news_md'
spacy_model_lg = iso639 + '_core_news_lg'

sentiment_lexicon_class = 'Sentix'

# Some lexicons provide a polarity of a token for each part of speech that token may have in the speech.
# If not None, only the polarities for the parts of speech in 'pos_token_sentiment' will be considered.
pos_token_sentiment = ['ADJ', 'ADV', 'VERB', 'NOUN', 'PROPN']

negations = ['nemmeno', 'neppure', 'neanche', 'nessuno', 'alcuno', 'veruno', 'niuno', 'niente', 'nulla', 'affatto',
             'mica', 'meno', 'mai più', 'figurati', 'figurarsi', 'mai', 'no', 'né', 'nè']
