"""
Thank you:

https://github.com/Kemaweyan/singleton_decorator
"""
class _SingletonWrapper:
    """
    Singleton wrapper class that creates instances
    for each decorated class.
    """

    def __init__(
        self,
        cls
    ):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(
        self,
        *args,
        **kwargs
    ):
        """
        Get a single instance of decorated class.
        """
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)

        return self._instance
