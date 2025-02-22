from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.text.transformer import remove_marks_and_accents


class TextFinderMode(Enum):
    """
    This is the mode in which we will look for the terms
    in the given segment text to find any coincidences.
    """

    EXACT = 'exact'
    """
    The term found must be exactly matched on the text,
    which means that accents and punctuation marks will
    be considered.
    """
    IGNORE_CASE_AND_ACCENTS = 'ignore_case_and_accents'
    """
    The term found must match, in lower case and ignoring
    the accents, the text.
    """

class TextFinder:
    """
    Class to simplify the way we look for texts
    within other texts.
    """

    @staticmethod
    def find_in_text(
        term: str,
        text: str,
        mode: TextFinderMode = TextFinderMode.IGNORE_CASE_AND_ACCENTS
    ):
        """
        Find the provided 'term' in the also provided
        'text' and obtain the start and end indexes
        of the 'term' according to that 'text'. The 
        term can be more than once in the 'text'.

        TODO: Add an ilustrative example.

        This method returns an array containing tuples
        with the start and end indexes of the term
        positions in which it has been found.
        """
        if not PythonValidator.is_string(term):
            raise Exception('The provided "term" is not a valid string.')
        
        if not PythonValidator.is_string(text):
            raise Exception('The provided "text" is not a valid string.')

        mode = TextFinderMode.to_enum(mode)

        if mode == TextFinderMode.IGNORE_CASE_AND_ACCENTS:
            term = remove_marks_and_accents(term).lower()
            text = remove_marks_and_accents(text).lower()

        text_words = text.split()
        term_words = term.split()
        
        # Store first and last index if found
        return [
            (i, i + len(term_words) - 1)
            for i in range(len(text_words) - len(term_words) + 1)
            if text_words[i:i + len(term_words)] == term_words
        ]