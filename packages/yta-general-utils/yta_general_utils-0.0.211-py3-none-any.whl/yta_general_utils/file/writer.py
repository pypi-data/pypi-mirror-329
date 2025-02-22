from yta_general_utils.programming.validator import PythonValidator
from requests import Response

import json


class FileWriter:
    """
    Class to simplify and encapsulate the functionality related with
    writting files.
    """

    @staticmethod
    def write_binary_file(
        binary_data: bytes,
        filename: str
    ):
        """
        Writes the provided 'binary_data' in the 'filename' file. It replaces the
        previous content if existing.
        """
        if binary_data is None:
            raise Exception('The provided "binary_data" parameter is not valid.')
        
        if not PythonValidator.is_string(filename):
            raise Exception('The provided "filename" parameter is not a valid string.')
        
        f = open(filename, 'wb')
        f.write(binary_data)
        f.close()

    @staticmethod
    def write_json_to_file(
        dict: dict,
        filename: str
    ):
        """
        Writes the provided 'dict' as a json into the 'filename'.

        @param
            **dict**
            Python dictionary that will be stored as a json.

            **filename**
            File path in which we are going to store the information.
        """
        if dict is None:
            raise Exception('The provided "dict" parameter is not valid.')
        
        if not PythonValidator.is_string(filename):
            raise Exception('The provided "filename" parameter is not a valid string.')
        
        return FileWriter.write_file(json.dumps(dict, indent = 4), filename)

    @staticmethod
    def write_file(
        text: str,
        output_filename: str
    ):
        """
        Writes the provided 'text' in the 'filename' file. It
        replaces the previous content if existing.
        """
        if not PythonValidator.is_string(text):
            raise Exception('The provided "text" parameter is not a valid string.')
        
        if not PythonValidator.is_string(output_filename):
            raise Exception('The provided "output_filename" parameter is not a valid string.')

        f = open(output_filename, 'w', encoding = 'utf8')
        f.write(text)
        f.close()

        return output_filename

    @staticmethod
    def write_file_by_chunks_from_response(
        response: Response,
        output_filename: str
    ):
        """
        Iterates over the provided 'response' and writes its content
        chunk by chunk in the also provided 'output_filename'.

        TODO: If you find a better way to handle this you are free to
        create new methods and move them into a new file.
        """
        if not PythonValidator.is_instanec(response, Response):
            raise Exception('The provided "response" parameter is not a Response instance.')
        
        if not PythonValidator.is_string(output_filename):
            raise Exception('The provided "output_filename" parameter is not a valid string.')
        
        CHUNK_SIZE = 32768

        # TODO: Make this method work with a common Iterator parameter
        # and not an specific response, please
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return output_filename