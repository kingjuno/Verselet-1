from typing import *
from compling.config import ConfigManager
import compling.lexicalAnalysis.tokenization.document_abc as abcdoc
from compling.lexicalAnalysis.tokenization.impl.paragraph import Paragraph
from compling.descriptor import f2att


class Document(abcdoc.Document):
    def __init__(self, doc_id: int, para_list: List[Paragraph], config: ConfigManager, metadata: dict) -> None:
        """
        Represents a generic document, which is a sequence of paragraph in the input.
        A document is identified by grouping a list of paragraph.

        Args:
           doc_id (int): unique document identifier.
           para_list (List[Paragraph]): The list of paragraphs making up the document.
           config (ConfigManager): a ConfigManager object.
           metadata (dict): token metadata as a key-value pairs.

        Returns:
           None.
       """

        # unique identifiers
        self.doc_id_ = doc_id

        # document
        self.text_ = " . ".join([sentence.text() for sentence in para_list])

        # paragraph list
        self.para_list = para_list

        # add some field only if the value in config.ini file is True
        for k, v in config.get_section(s='Document_record').items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metaddata for this document record
        self.add_metadata(metadata)

    def lang(self) -> str:
        return self.para_list[0].lang()

    @f2att
    def sentiment(self) -> Dict[str, float]:

        sentiment_values = {'pos': 0.0, 'neg': 0.0}
        count_gt0 = {'pos': 0, 'neg': 0}

        for para in self.para_list:
            for k in sentiment_values.keys():
                if para.sentiment()[k] > 0:
                    count_gt0[k] += 1
                sentiment_values[k] += para.sentiment()[k]

        for k in sentiment_values.keys():
            if count_gt0[k] > 0:
                if k in ("pos", "neg"):
                    sentiment_values[k] /= max(count_gt0["pos"], count_gt0["neg"])
                else:
                    sentiment_values[k] /= count_gt0[k]

        return sentiment_values

    @f2att
    def named_entities(self) -> List[Dict[str, Union[str, int]]]:

        named_entities = list()
        for i, para in enumerate(self.para_list):
            for j, sent in enumerate(para.sent_list):
                offset = para.sent_list[j].token_list[0].doc_pos_

                for ne in sent.named_entities():
                    ne_ = dict()
                    ne_['doc_pos_start_'] = ne['sent_pos_start_'] + offset
                    ne_['doc_pos_end_'] = ne['sent_pos_end_'] + offset
                    ne_['text_'] = ne['text_']
                    named_entities.append(ne_)

        return named_entities

    def text(self) -> str:
        return self.text_

    def lower(self) -> str:
        return self.text_.lower()

    @f2att
    def lemma(self) -> str:
        return " . ".join([sentence.lemma() for sentence in self.para_list])

    @f2att
    def negations(self) -> str:
        return " . ".join([para.negations() for para in self.para_list])

    @f2att
    def stem(self) -> str:
        return " . ".join([sentence.stem() for sentence in self.para_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the document."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)

    def to_dict(self) -> dict:
        """Converts the document to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
