from tqdm import tqdm
import copy
import math
from typing import *
from collections import defaultdict
from compling.lexicalAnalysis.vectorization import vectorization


class Vectorizer(vectorization.Vectorization):
    """
    The process of converting text into vector is called vectorization.
    The set of corpus documents vectorized corpus makes up the Vector Space Model, which can have a sparse or
    dense representation.

    A Vectorizer object allows you to create vectors grouping tokens for arbitrary fields.

    Grouping tokens by:

       * _doc_id_: you 're creating document vectors;
       * _sent_id_: you 're creating sentence vectors;
       * _author_: you're creating author vectors (each token must have an 'author' field);
       ...

    You can group by multiple fields.

    You can also choose the text field the tokens will be grouped by too. (e.g. lemma, text, stem, ...)

    It offers several functions to set the vector components values, such as:

       * **One-hot encoding** (binary values 0/1);
       * **Tf** (Term Frequency);
       * **TfIdf** (Term Frequency Inverse Document Frequency);
       * **MI** (Mutual Information)

    You can specify the vectorization representation format: Term x Document matrix, Postings list.
    """

    def postings2docterm(self, postings: Dict[str, dict]) -> Iterable[dict]:
        """
        Converts a postings list to docterm matrix.

        Args:
            postings (Dict[str, dict]): Postings list.
        """

        docterm = defaultdict(dict)
        for token in postings:
            for doc, relevance in postings[token].items():
                docterm[doc].update({token: relevance})

        for doc in docterm:
            yield {self.group_by_field_key: doc, 'bow': docterm[doc]}

    def docterm2postings(self, docterm: Iterable[dict]) -> Dict[str, dict]:
        """
        Converts a docterm matrix to a postings list.

        Args:
            docterm (Iterator[dict]): Docterm matrix.
        """

        postings = defaultdict(dict)
        for record in docterm:
            for token, relevance in record['bow'].items():
                postings[token].update({record[self.group_by_field_key]: relevance})

        return postings

    def tf(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
           dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
           min_count: int = 0, format_: str = "docterm-matrix", boolean=False) -> Union[Dict[str, dict], Iterable[dict]]:


        if not hasattr(self, 'tf_postings') or boolean:
            filters = dict()
            for k, v in self.nlp.config.get_section(s='Vector_filter').items():
                if v != 'None':
                    filters[k] = bool(int(v))

            def __filter__(__token__):
                for key, value in {'dep_': dep, 'pos_': pos}.items():
                    if value is not None and len(value) != 0 and __token__[key] not in value:
                        return False

                if len(__token__[self.token_field]) < min_len:
                    return False

                for key, value in filters.items():
                    if not __token__[key + '_'] == value:
                        return False

                if lang is not None and lang != __token__['lang_']:
                    return False

                return True

            postings = defaultdict(lambda: defaultdict(int))
            for token in tqdm(tokens, desc="TF calculation in progress...", position=0, leave=True):
                if not __filter__(token):
                    continue

                key = " + ".join([str(token[g]) for g in self.group_by_field])

                # replace . (ngrams like "commissione_._signore")
                token_field = token[self.token_field]
                if boolean:
                    postings[token_field][key] = 1
                else:
                    postings[token_field][key] += 1

            for token in copy.deepcopy(postings):
                if sum(postings[token].values()) < min_count:
                    del postings[token]

            if boolean:
                if format_ == 'postings-list':
                    return postings
                else:
                    return self.postings2docterm(postings)

            self.tf_postings = postings


        if format_ == 'postings-list':
            return self.tf_postings
        else:
            return self.postings2docterm(self.tf_postings)

    def reset_tf(self):
        """If present, removes the tf postings list from memory.
         It will be re-calculated on the next run call."""
        if hasattr(self, 'tf_postings'):
            delattr(self, 'tf_postings')

    def tfidf(self, tokens: Iterable[dict], normalize=True,
              pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
              dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
              min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:

        postings = self.tf(tokens, pos, dep, lang, min_len, min_count, format_='postings-list')

        docterm = self.postings2docterm(postings)
        max_tf = {}
        n = 0
        for doc in docterm:
            n += 1
            max_tf[doc[self.group_by_field_key]] = max(doc['bow'].values())

        # Corpus size: the number of documents in the corpus
        N = n

        # The tf_dict will be update to tfidf_dict
        tfidf_postings = copy.deepcopy(postings)

        bar = tqdm(total=len(tfidf_postings), desc="TFIDF calculation in progress... ", position=0, leave=True)

        # For each token in the postings list
        for token in tfidf_postings.keys():

            docs = tfidf_postings[token]

            # For each doc which the token occurs in
            for doc, tf in docs.items():
                if normalize:
                    tf = tf / max_tf[doc]

                # Document Frequency
                df = len(postings[token])

                # Inverse Document Frequency
                idf = math.log(N / df)

                # Term Frequency Inverse Document Frequency
                tfidf_postings[token].update({doc: tf * idf})
            bar.update(1)
        bar.close()

        if format_ == 'postings-list':
            return tfidf_postings
        else:
            return self.postings2docterm(tfidf_postings)

    def mi(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
           dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
           min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterator[dict]]:


        postings = self.tf(tokens, pos, dep, lang, min_len, min_count, format_='postings-list')
        docterm = {record[self.group_by_field_key]: record for record in self.postings2docterm(postings)}

        # x: group_by_field label
        # y: token
        n_tokens = sum([sum(postings[token].values()) for token in postings])

        mi_postings = defaultdict(lambda :defaultdict(int))
        for token in tqdm(postings, desc="Mutual Information calculation in progress...", position=0, leave=True):
            posting = defaultdict(int, postings[token])
            for label in posting:
                row = docterm[label]['bow']
                len_x = sum(posting.values())
                len_y = sum(row.values())

                p_x = len_x/n_tokens
                p_y = len_y/n_tokens
                p_x_y = posting[label]/n_tokens

                mi_postings[token][label] = p_x_y * math.log(p_x_y/(p_x*p_y))

        if format_ == 'postings-list':
            return mi_postings
        else:
            return self.postings2docterm(mi_postings)

    def onehot(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
               dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
               min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:

        return self.tf(tokens, pos, dep, lang, min_len, min_count, boolean=True, format_=format_)

    def run(self, mode: str, tokens: Iterable[dict], normalize=True,
            pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
            dep: Tuple[str, ...] = None,
            lang: str = None, min_len=0, min_count=0,
            metadata: Dict[str, dict] = None) -> Iterable[dict]:

        # in order to load the vectorization in a mongodb database
        if mode in ['tf', 'onehot']:
            docterm = getattr(self, mode)(tokens=tokens, pos=pos, dep=dep, lang=lang, min_len=min_len,
                                          min_count=min_count, format_='docterm-matrix')

        elif mode == 'tfidf':
            docterm = getattr(self, mode)(tokens=tokens, normalize=normalize, pos=pos, dep=dep, lang=lang,
                                          min_len=min_len, min_count=min_count,
                                          format_='docterm-matrix')

        # elif mode == 'mi':
        else:
            docterm = getattr(self, mode)(tokens=tokens, pos=pos, dep=dep, lang=lang, min_len=min_len,
                                          min_count=min_count,
                                          format_='docterm-matrix')

        # keep the information
        if metadata is not None and len(metadata) > 0:
            for row in docterm:
                if len(row['bow']) == 0:
                    continue
                record = dict(row)
                record.update(metadata[row[self.group_by_field_key]])
                yield record
        else:
            for row in docterm:
                if len(row['bow']) > 0:
                    yield row
