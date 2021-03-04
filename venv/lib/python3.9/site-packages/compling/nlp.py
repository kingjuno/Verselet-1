import unidecode
import sys
import re
import spacy
import string
import unicodedata
from spacy.tokens.doc import Doc
from nltk.corpus import stopwords
from collections import defaultdict
from typing import *
from nltk.stem.snowball import SnowballStemmer
from compling.config import ConfigManager


class NLP:
    """
    Natural Language Processing (_NLP_) is a field of _Artificial Intelligence_ that gives the machines the ability to
    read, understand and derive meaning from human languages. It is a discipline that focuses on the interaction between
    data science and human language.
    """

    def __init__(self) -> None:

        # configuration
        self.config = ConfigManager()
        language = self.config.get(s='Corpus', k='language')

        # language module
        module = __import__('compling.languages.{}'.format(language))
        nlp_language = getattr(getattr(module, 'languages'), language)
        self.nlp_language = nlp_language

        # spacy model
        spacy_model_size = self.config.get(s='Corpus', k='spacy_model_size')
        spacy_model_available = {size: getattr(nlp_language, 'spacy_model_{}'.format(size))
                                 for size in ['sm', 'md', 'lg']}
        spacy_model = spacy_model_available[spacy_model_size]

        # natural language processing tool
        self.nlp_spacy = spacy.load(spacy_model)

        # language
        self.language = language

        # stemmer
        self.stemmer = SnowballStemmer(language)

        # punctuation list
        # ascii punctuation characters
        punctuation = string.punctuation
        # unicode punctuation characters
        punctuation += "".join([chr(i) for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P')])
        self.punctuation = punctuation

        # lexicon
        if nlp_language.sentiment_lexicon_class is not None:
            module = __import__('compling.lexicons')
            self.lexicon = getattr(getattr(module, 'lexicons'), nlp_language.sentiment_lexicon_class)()
        else:
            # no lexicon available
            self.lexicon = None
            print('WARNING: No {} lexicon is available'.format(language))

    def is_stopword(self, token: str) -> bool:
        """
        Returns True if the input token is a stopword, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a stopword, else False.
        """

        return token in self.stopwords_list()

    def token_sentiment(self, token: str) -> dict:
        """Returns the token polarities (positive, negative, neutral)."""

        return self.lexicon.polarity(token)

    @staticmethod
    def is_ngram(token: str, sep: str = '_', n: int = None) -> bool:
        """
        Returns True if the input token is a stopword, else False.

        Args:
            token (str): Text of the token that has to be checked.
            sep (str, optional, default=_): The character separator that splits the n-gram into tokens.
            n (int, optional, default=None): If not None, checks if the input token is a n-gram of size n.

        Returns:
            bool: True, if the token is a n-gram, else False.
        """
        return token.count(sep) > 0 if n is None else token.count(sep) == n - 1

    @staticmethod
    def is_too_short(text: Union[str, list], min_len: int) -> bool:
        """
        If text is instance of str, returns True if text is less than 'min_len' characters long else False.
        If text is isntance of list, return True if text is less than 'min_len' tokens long else False.

        Args:
            text (Union[str, List[str]]): The input text that has to be checked.
            min_len (int, optional, default=0): Threshold: minimun length

        Returns:
            bool: True, if text is too short, else False.
        """
        return len(text) <= min_len

    @staticmethod
    def is_lower(text: str) -> bool:
        """
        Returns True if text is a lowercase string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a lowercase string, False otherwise.
        """

        return text.islower()

    @staticmethod
    def is_upper(text: str) -> bool:
        """
        Returns True if text is a uppercase string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a uppercase string, False otherwise.
        """
        return text.isupper()

    @staticmethod
    def is_capitalize(text: str) -> bool:
        """
        Returns True if text is a capitalize string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a capitalize string, False otherwise.
        """

        if len(text) < 2:
            return False

        return True if text[0].isupper() and text[1:].islower() else False

    @staticmethod
    def is_title(text: str) -> bool:
        """
        Returns True if text is a title string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a title string, False otherwise.
        """
        return text.istitle()

    @staticmethod
    def is_digit(token: str) -> bool:
        """
        Returns True if token is a digit string, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a digit string, False otherwise.
        """
        return token.isdigit()

    def is_punct(self, token: str) -> bool:
        """
        Returns True if token is a punctuation character, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a punctuation character, False otherwise.
        """
        return token in self.punctuation

    @staticmethod
    def is_space(token: str) -> bool:
        """
        Returns True if token is a space character, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a space character, False otherwise.
        """
        return token in string.whitespace

    def strip_punctuation(self, text: str, keep: Iterable[str] = None, sc: Iterable[str] = None) -> str:
        """
        Strips punctuation characters from a input text.

        Args:
            text (str): The input text.
            keep (Tuple[str, ...], optional, default=None): Punctuation characters to keep: they won't be stripped.
            sc (Tuple[str, ...], optional, default=None): Additional Special characters to be stripped.

        Returns:
            str: The text without punctuation characters.
        """

        if keep is not None and len(keep) > 0:
            punctuation = "".join([i for i in self.punctuation if i not in keep])
        else:
            punctuation = self.punctuation

        if sc is not None and len(sc) > 0:
            punctuation += "".join(sc)

        if keep is not None:
            text = text.translate(str.maketrans({k: ' {} '.format(k) for k in keep}))

        return self.strip_double_spaces(text.translate(str.maketrans(dict.fromkeys(punctuation, ' '))).strip())

    @staticmethod
    def strip_double_spaces(text):
        return " ".join(text.split())

    @staticmethod
    def strip_accents(text: str) -> str:
        """
        Strips accents from a input text.

        Args:
            text (str): The input text.

        Returns:
            str: The text without accents characters.
        """
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').strip()

    def strip_stopwords(self, text: str, min_len: int = 0) -> str:
        """
        Strips accents from a input text.

        Args:
            text (str): The input text.
            min_len (int, optional, default=0): Tokens shorter than min_len are stripped as stopwords.

        Returns:
            str: The text without accents characters.
        """
        return " ".join(
            [token for token in text.split() if not self.is_stopword(token) and len(token) >= min_len]).lower()

    @staticmethod
    def lower(text: str) -> str:
        """
        Returns a copy of the string converted to lowercase.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to lowercase.
        """
        return text.lower()

    @staticmethod
    def upper(text: str) -> str:
        """
        Returns a copy of the string converted to uppercase.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to uppercase.
        """
        return text.upper()

    @staticmethod
    def capitalize(text: str) -> str:
        """
        Returns a copy of the string converted to capitalize.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to capitalize.
        """
        return text.capitalize()

    @staticmethod
    def title(text: str) -> str:
        """
        Returns a copy of the string converted to title.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to title.
        """
        return text.title()

    def stem(self, token: str) -> str:
        """
        Strips affixes from the token and returns the stem.

        Args:
            token (str): The text of the input token.

        Returns:
            str: Returns the stem of the token.
        """
        return self.stemmer.stem(token)

    def split_skipgram(self, text: str, ws: int = 3) -> List[str]:
        """
        Returns a list of tokens as union of the tokens of each skipgrams pair.

        Args:
            text (str): The input text.
            ws (int, optional, default=3): Window size: size of sampling windows. <br/> The window of a word w_i will be [i-window_size, i+window_size+1]

        Returns:
            List[str]: A list of tokens as union of the tokens of each skipgrams pair.

                    Example:
                    >> nlp = NLP()
                    >> nlp.split_skipgram(text="My mistress' eyes are nothing like the sun", ws=2)
        """

        tokens = list()
        for skipgram in self.skipgrams(text, ws):
            tokens.extend(skipgram)
        return tokens

    def stopwords_list(self, include: Iterable[str] = None) -> List[str]:
        """
        Returns a stopwords list.

        Args:
            include (List[str], optional, default=None): Include a list of arbitrary stopwords.

        Returns:
            List[str]: a list of stopwords.
        """

        if not hasattr(self, 'stopwords'):
            self.stopwords = stopwords.words(self.language)
            if include is not None:
                self.stopwords.extend([s.lower() for s in include])

        return self.stopwords

    def ngrams(self, text: str, n: int, pos: Iterable[str] = ("PROPN", "VERB", "NOUN", "ADJ"),
               threshold: int = 50) -> Dict[str, int]:
        """
        Returns the most frequent n-grams in the text.

        Args:
            text (str): Input text.
            n (int): The size of n-grams: number of sequential strings that make up n-grams.
            pos (Tuple[str, ...], optional, default=PROPN,VERB,NOUN,ADJ): Part of speech of the first and the last token that make up n-grams. <br/> Filters the most informative n-grams. <br/> If None, the filter will be ignored.
            threshold (int, optional, default=50): Filters n-grams that have a frequency greater than threshold.

        Returns:
             Dict[str, int]: N-grams as keys, frequencies as values.
        """

        # Ngrams dict {ngram: frequency}
        ngram_frequencies = defaultdict(lambda: 1)

        # Scan of each source using a Sliding Window
        # Index Sliding Window
        c = 0

        # From text source to token list
        tokens = text.split()

        # Shift the Sliding Window until it covers the last token
        while c < len(tokens) - (n - 1):
            c += 1

            # First and last word can't be stopwords
            if self.is_stopword(tokens[c - 1]) or \
                    self.is_stopword(tokens[c + (n - 1) - 1]):
                continue

            ngram = tuple([tokens[c + i - 1] for i in range(0, n)])
            ngram_frequencies[ngram] = ngram_frequencies[ngram] + 1

        # Select the n grams you're interested in
        ngram_frequencies = {ngram: frequency for ngram, frequency in ngram_frequencies.items() if
                             frequency > threshold}

        if pos is None or len(pos) == 0:
            return ngram_frequencies

        # Ngram final list
        result = defaultdict(int)

        # First and last word must be in pos
        for ngram in ngram_frequencies:
            ngram_ = self.nlp_spacy(" ".join(ngram))
            if ngram_[0].pos_ in pos and ngram_[-1].pos_ in pos:
                ngram_ = " ".join([token.text for token in ngram_])
                result[ngram_] = ngram_frequencies[ngram]

        return result

    @staticmethod
    def skipgrams(text: str, ws: int = 3) -> List[Tuple[str, str]]:
        """
        Generates skipgram word pairs.

        Args:
            text (str): The input text.
            ws (int, optional, default=3): Window size: size of sampling windows. <br/> The window of a word w_i will be [i-window_size, i+window_size+1]

        Returns:
            List[Tuple[str, str]]: A list of tuple (skipgram pairs).
        """

        skipgrams = []
        tokens = text.split()

        ws += 1
        for i in range(0, len(tokens) - 1):
            for j in range(1, ws + 1):
                if i != len(tokens) - j and i + j < len(tokens):
                    skipgrams.append((tokens[i], tokens[i + j]))

        return skipgrams

    def named_entities(self, text: str) -> List[Dict[str, Union[str, int]]]:
        """
        Returns a list of named entities in text.

        Args:
            text (str): The input text.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of named entities. Each named entity is a dict with three keys:

                * _text_: the named entity
                * _start_: the position of the first token of the Named Entities in the text.
                * _end_: the position of the last token of the Named Entities in the text.
        """

        # cler text
        text = unidecode.unidecode(text)
        #text = self.strip_punctuation(text)

        if len(text) < 2:
            return []

        # find Named Entities by regex
        #"(?:(?<=^)|(?<=[^.]))\s+([A-Z]\w+)"
        named_entities = [{'start': m.start(0), 'end': m.end(0), 'text': m.group(0)}
                          for m in re.finditer("([A-Z]+[a-z]*)", text[0].capitalize() + text[1:], re.UNICODE)
                          if not self.is_stopword(m.group(0).lower())]

        text_spans = self.spans(text)

        # One or less named entities
        if len(named_entities) == 0:
            return list()
        elif len(named_entities) == 1:
            # pos start, pos end for each named entities
            for k, v in text_spans.items():
                if named_entities[0]['start'] in range(*k):
                    named_entities[0]['start'] = v
                    break

            for k, v in text_spans.items():
                if (named_entities[0]['end'] - 1) in range(*k):
                    named_entities[0]['end'] = v
                    break
            return [named_entities[0]]

        # Link consecutive named entities
        result = [named_entities[0]]
        for named_entity in named_entities[1:]:
            if result[-1]['end'] == named_entity['start'] - 1:
                result[-1]['text'] += " "+named_entity['text']
                result[-1]['end'] = named_entity['end']
            else:
                result.append(named_entity)

        # pos start, pos end for each named entities
        for ne in result:
            for k, v in text_spans.items():
                if ne['start'] in range(*k):
                    ne['start'] = v
                    break

            for k, v in text_spans.items():
                if (ne['end'] - 1) in range(*k):
                    ne['end'] = v
                    break
        return result

    def spacy_named_entities(self, text: str) -> List[Dict[str, Union[str, int]]]:
        """
        Returns a list of named entities in text recognized by spacy.

        Args:
            text (str): The input text.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of named entities. Each named entity is a dict with three keys:

                * _text_: the named entity
                * _start_: the position of the first token of the Named Entities in the text.
                * _end_: the position of the last token of the Named Entities in the text.
        """

        named_entities = []
        for ent in self.nlp_spacy(text).ents:
            named_entity = dict()
            named_entity['text'] = ent.text
            named_entity['start'] = -1
            named_entity['end'] = -1

            character_index = 0
            for token_index, token in enumerate(text.split()):
                for _ in token:
                    if ent.start_char == character_index:
                        named_entity['start'] = token_index
                    if ent.end_char == character_index + 1:
                        named_entity['end'] = token_index
                    character_index += 1

                # whitespace character
                character_index += 1

                if named_entity['start'] >= 0 and named_entity['end'] >= 0:
                    break

            named_entities.append(named_entity)

        return named_entities

    @staticmethod
    def spans(text: str) -> Dict[Tuple[int, int], int]:
        """
        Returns the starting and ending character index for each token in the text.

        Args:
            text (str): The input text.

        Returns:
            Dict[Tuple[int, int], int]: A dict containing the the starting and ending character index for each token in the text as keys;
            and the token index for each token in text as values.
        """

        result = dict()
        point = 0  # Where we're in the text.

        for t, fragment in enumerate(text.split()):
            found_start = text.index(fragment, point)
            found_end = found_start + len(fragment)
            result[(found_start, found_end)] = t
            point = found_end

        return result

    def negated_tokens(self, text: Union[str, Doc]) -> List[bool]:
        """Returns a mask that specifies which tokens are negated in the text.

        Args:
            text (Union[str, spacy.tokens.doc.Doc]): The input text that has to be analyzed.

        Returns:
            bool: A mask that specifies which tokens are negated in the text.
        """

        tokens = text if type(text) is Doc else self.nlp_spacy(text)
        mask, negated = [], []

        # All children tokens linked to a parent token by a negation relationship
        for token in tokens:
            if token.dep_ == "neg" or token.text in self.nlp_language.negations:
                negated += [x for x in token.head.children] + [token.head]

        for token in tokens:

            # All children tokens linked to a parent token by a negation relationship and
            # All tokens attached to a modifying adjective or adverb
            if (token in negated or (token.dep_ in ["amod", "advmod"] and token.head in negated)) and \
                    token.text not in self.nlp_language.negations:
                mask.append(True)
                continue

            mask.append(False)
        return mask