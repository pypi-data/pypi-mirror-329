"""
Class to dynamically obtain the attributes in
an instance.
"""

class AttributeObtainer:
    """
    Class to interact with an instance and dynamically obtain
    the attributes that have been set. This is useful to 
    dynamically call methods that need those parameters.
    """

    @staticmethod
    def get_attributes_from_instance(
        instance: object,
        attributes_to_ignore: list[str] = []
    ):
        """
        Obtain the attributes of the given 'instance'
        as a dict containing the keys and values of
        these attributes.

        Only the values that are actually set on the
        instance are obtained with 'vars'. If you set
        'var_name = None' but you don't do 
        'self.var_name = 33' in the '__init__' method,
        it won't be returned by the 'vars()' method.
        """
        # Each attribute is a dict 'key: value'
        return {
            k: v
            for k, v in vars(instance).items()
            if k not in attributes_to_ignore
        }
