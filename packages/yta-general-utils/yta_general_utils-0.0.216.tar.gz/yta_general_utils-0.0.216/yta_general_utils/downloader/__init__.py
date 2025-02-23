from yta_general_utils.programming.output import Output
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.file.enums import FileTypeX, FileExtension
from yta_general_utils.downloader.audio import download_audio
from yta_general_utils.downloader.gif import download_gif
from yta_general_utils.downloader.google_drive import GoogleDriveResource
from yta_general_utils.downloader.image import download_image_2
from yta_general_utils.downloader.video import download_video
from yta_general_utils.downloader.utils import download_file
from yta_general_utils.dataclasses import FileReturn
from typing import Union


# TODO: Make all submethods return the element read (image as Pillow,
# video as VideoFileClip or numpy, etc. and also the filename
class Downloader:
    """
    Class to encapsulate the functionality related to download resources
    from the Internet.
    """

    # TODO: Maybe move the checkings to the specific 'download_x' method
    # and not here that is more a encapsulation class
    @staticmethod
    def download_audio(
        url: str,
        output_filename: Union[str, None] = None
    ):
        """
        Download the audio file from the provided 'url' and stores
        it locally as 'output_filename'.
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')

        # TODO: Add more checkings here (?)
        # I don't know the exception of the file
        return download_audio(url, Output.get_filename(output_filename, FileTypeX.AUDIO))
    
    @staticmethod
    def download_gif(
        query: str, 
        output_filename: Union[str, None] = None
    ):
        """
        Search for a gif with the provided 'query' and download it,
        if existing, to a local file called 'output_filename'.

        TODO: I think this is unexpected, because it is searching
        from Giphy and not downloading a file from a url as a gif...
        """
        if not PythonValidator.is_string(query):
            raise Exception('The provided "query" parameter is not a string.')

        return download_gif(query, Output.get_filename(output_filename, FileExtension.GIF))
    
    @staticmethod
    def download_google_drive_resource(
        google_drive_url: str,
        output_filename: Union[str, None] = None
    ):
        """
        Download the Google Drive resource from the given 'google_drive_url',
        if existing and available, to a local file called 'output_filename'.
        """
        if not PythonValidator.is_string(google_drive_url):
            raise Exception('The provided "google_drive_url" parameter is not a string.')
        
        # I don't know the exception of the file
        return GoogleDriveResource.download_from_url(google_drive_url, Output.get_filename(output_filename))
    
    @staticmethod
    def download_image(
        url: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download the image from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return download_image_2(url, Output.get_filename(output_filename))

    @staticmethod
    def download_video(
        url: str,
        output_filename: Union[str, None] = None
    ):
        """
        Download the video from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return download_video(url, Output.get_filename(output_filename))
    
    @staticmethod
    def download_file(
        url: str,
        output_filename: str
    ):
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        if output_filename is None:
            raise Exception(f'The "output_filename" parameter is mandatory as we do not know the file extension.')
        
        return download_file(url, output_filename)