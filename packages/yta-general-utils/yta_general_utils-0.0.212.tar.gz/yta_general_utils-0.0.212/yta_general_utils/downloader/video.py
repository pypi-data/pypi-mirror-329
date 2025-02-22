from yta_general_utils.downloader.utils import download_file
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.dataclasses import FileReturn
from typing import Union


def download_video(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturn:
    """
    Receives a downloadable url as 'url' and downloads that video in
    our system as 'output_filename'.
    """
    return download_file(url, Output.get_filename(output_filename, FileTypeX.VIDEO))