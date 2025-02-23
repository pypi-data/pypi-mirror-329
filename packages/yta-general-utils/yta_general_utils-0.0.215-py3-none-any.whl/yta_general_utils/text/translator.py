from yta_general_utils.web.scrapper.chrome_scrapper import google_translate
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


class GoogleTranslatorLanguage(Enum):
    """
    The language for the GoogleTranslator platform.
    """

    # TODO: Implement more languages
    ENGLISH = 'en'
    SPANISH = 'es'

# TODO: Create class GoogleTranslator to wrap this
def translate_text(
    text: str,
    input_language: Union[GoogleTranslatorLanguage, str] = GoogleTranslatorLanguage.ENGLISH,
    output_language: Union[GoogleTranslatorLanguage, str] = GoogleTranslatorLanguage.SPANISH
):
    """
    Returns the provided 'text' translated into the
    'output_language' using Google Traductor by chromedriver
    navigation.
    """
    if not PythonValidator.is_string(text):
        print('The provided "text" is not a valid string.')

    input_language = GoogleTranslatorLanguage.to_enum(input_language)
    output_language = GoogleTranslatorLanguage.to_enum(output_language)

    return google_translate(text, input_language.value, output_language.value)
