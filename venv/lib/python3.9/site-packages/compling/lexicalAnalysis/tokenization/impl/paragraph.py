from typing import *
from compling.config import ConfigManager
import compling.lexicalAnalysis.tokenization.paragraph_abc as abcpara
from compling.lexicalAnalysis.tokenization.impl.sentence import Sentence, f2att


class Paragraph(abcpara.Paragraph):
    def __init__(self, para_id: int, sent_list: List[Sentence], config: ConfigManager, metadata: dict) -> None:
        """
        Represents a generic paragraph, which is a sequence of sentence in the input.
        A paragraph is identified by grouping a list of sentence.

        Args:
           para_id (int): unique paragraph identifier.
           sent_list (List[Sentence]): The list of sentences making up the paragraph.
           config (ConfigManager): a ConfigManager object.
           metadata (dict): token metadata as a key-value pairs.

        Returns:
           None.
        """

        # unique identifiers
        self.para_id_ = para_id

        # paragraph
        self.text_ = " . ".join([sentence.text() for sentence in sent_list])

        # sentence list
        self.sent_list = sent_list

        # add some field only if the value in config.ini file is True
        for k, v in config.get_section(s='Paragraph_record').items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metadata for this paragraph record
        self.add_metadata(metadata)

    @f2att
    def named_entities(self) -> List[Dict[str, Union[str, int]]]:

        named_entities = list()
        for i, sent in enumerate(self.sent_list):
            offset = sent.token_list[0].para_pos_

            for ne in sent.named_entities():
                ne_ = dict()
                ne_['para_pos_start_'] = ne['sent_pos_start_'] + offset
                ne_['para_pos_end_'] = ne['sent_pos_end_'] + offset
                ne_['text_'] = ne['text_']
                named_entities.append(ne_)

        return named_entities

    def lang(self) -> str:
        return self.sent_list[0].lang()

    def text(self) -> str:
        return self.text_

    def lower(self) -> str:
        return self.text_.lower()

    @f2att
    def lemma(self) -> str:
        return " . ".join([sentence.lemma() for sentence in self.sent_list])

    @f2att
    def negations(self) -> str:
        return " . ".join([sent.negations() for sent in self.sent_list])

    @f2att
    def sentiment(self) -> Dict[str, float]:

        sentiment_values = {'pos': 0.0, 'neg': 0.0}
        count_gt0 = {'pos': 0, 'neg': 0}

        for sent in self.sent_list:
            for k in sentiment_values.keys():
                if sent.sentiment()[k] > 0:
                    count_gt0[k] += 1
                sentiment_values[k] += sent.sentiment()[k]

        for k in sentiment_values.keys():
            if count_gt0[k] > 0:
                if k in ("pos", "neg"):
                    sentiment_values[k] /= max(count_gt0["pos"], count_gt0["neg"])
                else:
                    sentiment_values[k] /= count_gt0[k]

        return sentiment_values

    @f2att
    def stem(self) -> str:
        return " . ".join([sentence.stem() for sentence in self.sent_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the paragraph."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)

    def to_dict(self) -> dict:
        """Converts the paragraph to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
