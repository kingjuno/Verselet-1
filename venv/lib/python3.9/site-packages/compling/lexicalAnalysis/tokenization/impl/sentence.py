from typing import *
from compling.nlp import NLP
from compling.config import ConfigManager
import compling.lexicalAnalysis.tokenization.sentence_abc as abcsent
from compling.lexicalAnalysis.tokenization.impl.token import Token, f2att


class Sentence(abcsent.Sentence):
    def __init__(self, sent_id: int,
                 token_id: int,
                 sent: str,
                 nlp: NLP,
                 config: ConfigManager,
                 para_id: int,
                 doc_id: int,
                 para_pos: int,
                 doc_pos: int,
                 metadata: dict) -> None:
        """
        Represents a generic sentence, which is a sequence of tokens in the input.
        A sentence is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
        of tokens.

        Args:
           sent_id (int): Unique sentence identifier.
           token_id (int): Unique token identifier. The token_id of the first token in the sentence.
           sent (str): Text of the sentence.
           nlp (NLP): A Natural Language Processing object.
           config (ConfigManager): A Config manager object.
           para_id (int): Unique paragraph identifier. The id of the paragraph the sentence occurs in.
           doc_id (int): Unique document identifier. The id of the document the sentence occurs in.
           para_pos (int): Position index in the paragraph of the first token in the sentence.
           doc_pos (int): Position index in the document of the first token in the sentence.
           metadata (dict): Token metadata as a key-value pairs.

        Returns:
           None.
        """

        # unique identifiers
        self.token_id = token_id
        self.sent_id_ = sent_id

        # Natural Language Object
        self.nlp = nlp

        # sentence
        self.text_ = sent

        # position index
        self.para_pos = para_pos
        self.doc_pos = doc_pos

        # token list
        sentence = nlp.nlp_spacy(sent)
        # find negated token
        negation_mask = nlp.negated_tokens(sentence)
        self.token_list = [Token(self.next_token_id(), token, nlp, config,
                                 sent_id, para_id, doc_id,
                                 sent_pos, self.next_para_pos(), self.next_doc_pos(), negation_mask[sent_pos], metadata)
                           for sent_pos, token in enumerate(sentence)]

        # add some field only if the value in config.ini file is True
        for k, v in config.get_section(s='Sentence_record').items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metadata for this sentence record
        self.add_metadata(metadata)

    @f2att
    def named_entities(self) -> List[Dict[str, Union[str, int]]]:

        named_entities = self.nlp.named_entities(self.text_)

        for ne_ in named_entities:
            ne_['sent_pos_start_'] = ne_.pop('start')
            ne_['sent_pos_end_'] = ne_.pop('end')
            ne_['text_'] = ne_.pop('text')

        # If n-grams are added in the text we don't want to find a named entities twice:
        # Examples:
        # Donald Trump __Donald_Trump__ made his speech in New York __New_York__
        # We don't want n-grams_entities:
        # [{'start': 0, 'end': 1, 'text': 'Donald Trump'}, {'start': 2, 'end': 2, 'text': 'Donald Trump'}, {'start': 7, 'end': 8, 'text': 'New York'}, {'start': 9, 'end': 9, 'text': 'New York'}]
        # We want ngram_entities_:
        # [{'start': 0, 'end': 1, 'text': 'Donald Trump'}, {'start': 7, 'end': 8, 'text': 'New York'}]

        if self.nlp.__ngrams_replaced__ == False:
            named_entities_ = list()
            for ne_ in named_entities:
                if ne_['sent_pos_start_'] == ne_['sent_pos_end_'] and len(ne_['text_'].split()) > 1:
                    continue
                else:
                    named_entities_.append(ne_)
            return named_entities_

        else:
            return named_entities

    def lang(self) -> str:
        return self.nlp.nlp_language.iso639

    def next_para_pos(self) -> int:
        """Returns the next token position in the paragraph."""
        self.para_pos += 1
        return self.para_pos

    def next_doc_pos(self) -> int:
        """Returns the next token position in the document."""
        self.doc_pos += 1
        return self.doc_pos

    def next_token_id(self) -> int:
        """Returns the next token id."""
        self.token_id += 1
        return self.token_id

    def text(self) -> str:
        return self.text_

    def lower(self) -> str:
        return self.text_.lower()

    @f2att
    def negations(self) -> str:

        text = lambda token: 'NOT_' + token.text() if token.is_negated_ else token.text()
        return " ".join([text(token) for token in self.token_list])

    @f2att
    def sentiment(self) -> Dict[str, float]:

        sentiment_values = {'pos': 0.0, 'neg': 0.0, 'obj': 0.0}
        count_gt0 = {'pos': 0, 'neg': 0, 'obj': 0.0}

        for token in self.token_list:
            for k in sentiment_values.keys():
                if token.sentiment()[k] > 0:
                    count_gt0[k] += 1
                sentiment_values[k] += token.sentiment()[k]

        for k in sentiment_values.keys():
            if count_gt0[k] > 0:
                if k in ("pos", "neg"):
                    sentiment_values[k] /= max(count_gt0["pos"], count_gt0["neg"])
                else:
                    sentiment_values[k] /= count_gt0[k]

        return sentiment_values

    @f2att
    def lemma(self) -> str:

        return " ".join([token.lemma() for token in self.token_list])

    @f2att
    def stem(self) -> str:

        return " ".join([token.stem() for token in self.token_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the sentence."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)
        for token in self.token_list:
            token.add_metadata(metadata)

    def to_dict(self) -> dict:
        """Converts the sentence to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
