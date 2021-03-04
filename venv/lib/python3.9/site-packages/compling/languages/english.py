language = 'english'
iso639 = 'en'

spacy_model_sm = iso639 + '_core_web_sm'
spacy_model_md = iso639 + '_core_web_md'
spacy_model_lg = iso639 + '_core_web_lg'

sentiment_lexicon_class = 'Sentiwordnet'

# Some lexicons provide a polarity of a token for each part of speech that token may have in the speech.
# If not None, only the polarities for the parts of speech in 'pos_token_sentiment' will be considered.
pos_token_sentiment = ['AUX', 'VERB', 'ADJ', 'ADV', 'NOUN', 'PROPN']

negations = ['not', "n't", 'no', 'none', 'neither', 'nor', 'never', 'hardly', 'scarcely',
             'barely', 'rarely', 'seldom', "doesn't", "isn't", "don't", "shouldn't", "couldn't",
             "won't", "can't", 'nobody', 'naught', 'nil', 'nix', 'nonentity', 'nullity', 'nothingness',
             'zilch']
