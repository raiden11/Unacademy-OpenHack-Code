"""Utilities
"""
import re
# from metaphone import doublemetaphone
# from vaakya.bootstrap import Bootstrap

# _bootstrap = Bootstrap()  # pylint: disable=invalid-name

## These puctuations does not contain + and # as they hold a special meaning
punctuations = '!"$%&\'()*,-./:;<=>?@[\\]^_`{|}~'    # pylint: disable=invalid-name
punctuations_for_none = '-\''    # pylint: disable=invalid-name

NONE_TRANSLATION_TABLE = dict.fromkeys(map(ord, punctuations), None)
SPACE_TRANSLATION_TABLE = dict.fromkeys(map(ord, punctuations), ord(' '))

PUNCTWISE_SPACE_TRANSLATION_TABLE = SPACE_TRANSLATION_TABLE.copy()
PUNCTWISE_NONE_TRANSLATION_TABLE = dict.fromkeys(map(ord, punctuations_for_none), None)

PUNCTWISE_TRANSLATION_TABLE = {}
PUNCTWISE_TRANSLATION_TABLE.update(PUNCTWISE_SPACE_TRANSLATION_TABLE)
PUNCTWISE_TRANSLATION_TABLE.update(PUNCTWISE_NONE_TRANSLATION_TABLE)


def chain(inputs, *funcs):
    """Chains multiple functions to be applied on an input
    consuming the return value as an input in next iteration
    """
    for func in funcs:
        inputs = (func() if not inputs else func(*inputs),)
    return inputs[0]


def _is_stopword(word):
    """Returns if given word `word` is a stopword

    NOTE: word should be lowercased
    """
    return _bootstrap.is_stopword(word)


def _is_in_vocab(word):
    """Returns if given word `word` is in vocabulary

    NOTE: word should be lowercased
    """
    return _bootstrap.is_in_vocab(word)


def _is_number(word):
    """Returns if given word `word` is a number
    """
    return bool(re.search(r'^\d+(.\d+)?(rd|st|nd|th)?$', word))


def _clean_puncts(text):
    """Cleans all the punctuation from the text
    """
    return text.translate(NONE_TRANSLATION_TABLE)


def _spaced_puncts(text):
    """Replaces punctuation with space in text
    """
    return text.translate(SPACE_TRANSLATION_TABLE)


def _puncts_based_repl(text):
    """Replaces puncts with either space/None depending on its
    own characteristric
    """
    return text.translate(PUNCTWISE_TRANSLATION_TABLE)


def _lower(text):
    """Returns the lowercased string
    """
    return text.lower()


def _remove_multiple_whitespace(text):
    """Removes and returns the text after removing multiple whitespaces
    """
    return u" ".join(text.split())


def cleanse(text):
    """Applies cleaning functions to the text and returns the cleaned version
    """
    return chain((text,), _lower, _puncts_based_repl, _remove_multiple_whitespace)


def cleanse_0(text):
    """Applies cleaning functions to the text and returns the cleaned version
    """
    return chain((text,), _lower, _remove_multiple_whitespace)


def tokenize(text):
    """Returns the text after splitting it on whitespace
    """
    return text.split()


def filter_stopwords(tokens):
    """Removes all the stopwords from list of tokens
    """
    return [token for token in tokens if not _is_stopword(token)]


def generate_metaphone(text):
    """Returns the metaphone for the given text. None is it is unable to generate any.
    """
    return doublemetaphone(text)[0]


def get_synonyms(word):
    """Returns synonyms of the word if given word is in vocabulary

    NOTE: word should be lowercased
    """
    return _bootstrap.get_synonyms(word)
