from typing import *
from tqdm import tqdm
from datetime import datetime
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from compling.lexicalAnalysis.tokenization import tokenization_abc
from collections.abc import Iterable as abciterable
from compling.lexicalAnalysis.tokenization.impl.sentence import Sentence
from compling.lexicalAnalysis.tokenization.impl.paragraph import Paragraph
from compling.lexicalAnalysis.tokenization.impl.document import Document


class Tokenizer(tokenization_abc.Tokenization):
    """
    Tokenization converts input text to streams of tokens, where each token is a separate word, punctuation sign,
    number/amount, date, etc.

    A Tokenizer object converts the corpus documents into a stream of:

       * _tokens_: tokens occurring in those documents. Each token is characterized by:
          * _token_id_: unique token identifier;
          * _sent_id_: unique sentence identifier. The id of the sentence the token occurs in;
          * _para_id_: unique paragraph identifier. The id of the paragraph the token occurs in;
          * _doc_id_: unique document identifier. The id of the document the token occurs in;
          * _text_: the text of the token;
          * a large variety of _optional meta-information_ (e.g. PoS tag, dep tag, lemma, stem, ...);
       * _sentences_ : sentences occurring in those documents. Each sentence is characterized by:
          * _sent_id_: unique sentence identifier;
          * _para_id_: unique paragraph identifier. The id of the paragraph the sentence occurs in;
          * _doc_id_: unique document identifier. The id of the document the sentence occurs in;
          * _text_: the text of the sentence;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
       * _paragraphs_: sentences occurring in those documents. Each paragraph is characterized by:
          * _para_id_: unique paragraph identifier;
          * _doc_id_: unique document identifier. The id of the document the paragraph occurs in;
          * _text_: the text of the paragraph;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
       * _documents_: Each document is characterized by:
          * _doc_id_: unique document identifier;
          * _text_: the text of the document;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);

    A Tokenizer object is also able to retrieve frequent n-grams to be considered as unique tokens.

    For each record (token, sentence, paragraph, document) are stored some metadata.
    You can edit the config.ini file to change those stored by default.

    In order to run tokenization you need to provide a Iterable[dict], where each document is a dict
    and has a key where it stores the text of the document. By default the text key is 'text', you can change it
    editing the config.ini file.

    For each document in your corpus, all key/value data (except for text key) are added as metadata to
    that document records. (e.g. title, author, ...).
    """

    def __init__(self, domain_stopwords: Iterable[str] = None) -> None:
        """
        Args:
            domain_stopwords (List[str], optional, default=None): You can provide a list of arbitrary stopwords specific to your corpus domain.
        """

        # super __init__
        super(Tokenizer, self).__init__()

        # add some stopwords to nlp list.
        self.nlp.stopwords_list(include=domain_stopwords)
        self.nlp.__ngrams_replaced__ = True

        self.corpus_ngrams = None

    def ngrams2tokens(self,
                      n: Union[int, Iterable[int]],
                      docs_in: Iterable[Dict[str, str]],
                      docs_out: Iterable[Dict[str, str]] = None,
                      pos: List[str] = ("PROPN", "VERB", "NOUN", "ADJ"),
                      corpus_threshold: int = 50,
                      doc_threshold: int = 0,
                      len_gram: int = 3,
                      include: List[str] = None,
                      replace: bool = False) -> Iterable[Dict[int, str]]:

        # list of sizes of n-grams
        if isinstance(n, abciterable):
            sizes = n
        else:  # isinstance(n, int):
            sizes = [n]

        ngram_frequencies = defaultdict(int)

        # for each corpus doc
        for doc in tqdm(docs_in, desc='N-gram Retrieval in progress...', position=0, leave=True):
            text = doc[self.text_key]
            for n in sizes:
                for ngram, frequency in self.nlp.ngrams(text, n, pos=tuple(), threshold=doc_threshold).items():
                    ngram_frequencies[ngram] += frequency

        # Select the n grams you're interested in
        ngram_frequencies = {ngram: frequency for ngram, frequency in ngram_frequencies.items() if
                             frequency >= corpus_threshold}

        # Ngram final list
        result = defaultdict(int)

        # First and last word must be in pos and at least len_gram sized
        for ngram in ngram_frequencies:
            ngram_ = self.nlp.nlp_spacy(" ".join(ngram))
            if ngram_[0].pos_ in pos and ngram_[-1].pos_ in pos and \
                    len(ngram_[0].text) >= len_gram and len(ngram_[-1].text) >= len_gram:
                ngram_ = " ".join([token.text for token in ngram_])
                result[ngram_] = ngram_frequencies[ngram]

        # add arbitrary n-grams
        if include is not None:
            for ngram in include:
                if ngram not in result:
                    result[ngram] = 0

        # sorted by len: first we replace the longer n-grams, then shorter ones.
        self.corpus_ngrams = dict(sorted(result.items(), key=lambda x: len(x[0]), reverse=True))

        # updates doc: replaces n-grams with tokens
        if docs_out is None:
            return

        if replace:
            self.nlp.__ngrams_replaced__ = replace

        for doc in docs_out:
            for ngram in self.corpus_ngrams:
                if replace:
                    doc[self.text_key] = doc[self.text_key].replace(ngram, "__" + ngram.replace(' ', '_') + "__")
                else:
                    doc[self.text_key] = doc[self.text_key].replace(ngram,
                                                                    ngram + ' __' + ngram.replace(' ', '_') + "__")
            yield doc

    def run(self,
            docs: Iterable[Dict[str, str]],
            doc_id: int = 0,
            token_id: int = 0,
            sent_id: int = 0,
            para_id: int = 0,
            para_size: int = 3,
            index_doc: bool = True,
            index_sent: bool = True,
            index_para: bool = True) -> Iterable[Dict[str, dict]]:

        # list of sentences making up a paragraph
        # list of paragraphs making up a document
        sent_list, para_list = list(), list()

        # SIDE EFFECT: Sentence will increment token_id by one, so that it can start from token_id and not from token_id+1 .
        token_id = token_id - 1

        # tokenization of each doc
        for doc in tqdm(docs, desc='Tokenization in progress...', position=0, leave=True):


            text = doc[self.text_key]

            metadata = dict()
            for k, v in doc.items():
                if k == self.text_key:
                    continue
                try:
                    # if it's a date
                    v = datetime.strptime(v, self.date_format)
                except:
                    if isinstance(v, str):
                        v = v.replace('.', '/')
                    pass
                metadata[k] = v

            # token position inside the paragraphs/documents: -1, Sentence will increment it, so that it can start from 0.
            para_pos, doc_pos = -1, -1

            # tokenization of each sentence
            for sent in sent_tokenize(text, language=self.nlp.language):
                sent = Sentence(sent_id, token_id, sent, self.nlp, self.nlp.config, para_id,
                                doc_id, para_pos, doc_pos, metadata)
                para_pos, doc_pos = sent.para_pos, sent.doc_pos
                sent_list.append(sent)

                # new paragraph
                if len(sent_list) == para_size:
                    para_list.append(Paragraph(para_id, sent_list, self.nlp.config, metadata))
                    sent_list = list()
                    # next paragraph
                    para_id += 1

                # next token
                token_id = sent.token_id
                # next sentence
                sent_id += 1

            # Reset sentence list. Remove item from the previous source.
            # The last paragraph can be shorter than the others.
            # new paragraph
            if len(sent_list) > 0:
                para_list.append(Paragraph(para_id, sent_list, self.nlp.config, metadata))
                para_id += 1
                sent_list = list()

            # new document
            doc = Document(doc_id, para_list, self.nlp.config, metadata)
            para_list = list()

            # next document
            doc_id += 1

            # build records
            doc_records, para_records, sent_records, token_records = list(), list(), list(), list()
            if index_doc:
                doc_records.append(doc.to_dict())
            if index_para:
                para_records.extend([para.to_dict() for para in doc.para_list])
            for para in doc.para_list:
                if index_sent:
                    sent_records.extend([sent.to_dict() for sent in para.sent_list])
                for sent in para.sent_list:
                    token_records.extend([token.to_dict() for token in sent.token_list])

            # store data in database
            tokenization_ = dict()
            tokenization_['tokens'] = token_records
            if index_sent:
                tokenization_['sentences'] = sent_records
            if index_para:
                tokenization_['paragraphs'] = para_records
            if index_doc:
                tokenization_['documents'] = doc_records

            yield tokenization_