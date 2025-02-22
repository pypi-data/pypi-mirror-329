from yta_general_utils.math.graphic.graphic import Graphic
from yta_general_utils.math.value_normalizer import ValueNormalizer
from yta_general_utils.programming.validator import PythonValidator


class RateFunctionGraphic:
    """
    A Graphic instance that uses itself as a rate
    function and returns the corresponding value
    for the given 'n'.

    TODO: Maybe force that the provided graphic 
    must end in the maximum Y value so, when
    normalized, it ends in value 1.
    """

    def __init__(
        self,
        graphic: Graphic
    ):
        if not PythonValidator.is_instance(graphic, Graphic):
            raise Exception('The "graphic" parameter provided is not a Graphic class instance.')

        self.graphic = graphic
        
    def get_n_value(
        self,
        n: float
    ):
        """
        Get the corresponding value for the given 'n' normalized
        value that must be between 0 and 1.
        """
        return ValueNormalizer(self.graphic.min_y, self.graphic.max_y).normalize(self.graphic.get_xy_from_normalized_d(n)[1])