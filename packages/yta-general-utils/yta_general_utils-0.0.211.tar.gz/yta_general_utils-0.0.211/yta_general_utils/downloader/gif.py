from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from random import choice
from typing import Union

import requests


GIPHY_API_KEY = Environment.get_current_project_env('GIPHY_API_KEY')

def download_gif(
    query: str,
    output_filename: Union[str, None] = None
):
    """
    Downloads a random GIF from Giphy platform using our API key. This gif is downloaded
    in the provided 'output_filename' (but forced to be .webp).

    This method returns None if no gif found, or the output filename with it's been
    locally stored.

    Check this logged in: https://developers.giphy.com/dashboard/
    """
    limit = 5

    url = "http://api.giphy.com/v1/gifs/search"
    url += '?q=' + query + '&api_key=' + GIPHY_API_KEY + '&limit=' + str(limit)

    response = requests.get(url)
    response = response.json()

    if not response or len(response['data']) == 0:
        # TODO: Raise exception of no gif found
        print('No gif "' + query + '" found')
        return None
    
    element = choice(response['data'])
    gif_url = 'https://i.giphy.com/' + element['id'] + '.webp'

    return download_image(gif_url, Output.get_filename(output_filename, FileExtension.WEBP))