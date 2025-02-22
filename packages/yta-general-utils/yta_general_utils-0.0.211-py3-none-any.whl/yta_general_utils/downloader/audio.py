from yta_general_utils.downloader.utils import download_file
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.output import Output
from typing import Union


def download_audio(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturn:
    """
    Receives a downloadable url as 'url' and downloads that audio in
    our system as 'output_filename'.

    This method will return the final 'output_filename' in which the
    file has been downloaded if so.
    """
    return download_file(url, Output.get_filename(output_filename, FileTypeX.AUDIO))