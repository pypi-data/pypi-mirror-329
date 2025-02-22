"""
Module to validate parameters, values, etc.

Some interesting information below:
The 'inspect' module (native in python) is very interesting because
it has some methods to check if a user defined function or things 
like that.

'f.__qualname__' is very interesting thing as it works
with the full path, not as 'f.__name__' does, this is
one example of it value when doing it from a local file:

'Example.example.__qualname__'
test_discord_video.<locals>.Example.example

And yes, the 'example' is a @staticmethod defined in the
Example class that is contained in the 'test_discord_video'
file
"""
from enum import Enum
from array import array
from typing import Union

import numpy as np
import inspect
import re


class PythonValidator:
    """
    Class to simplify and encapsulate the functionality related with
    parameters and variables validation.

    This class has been created to simplify the way it work and 
    replace the old ParameterValidator that was using too many 
    different methods being imported and generating cyclic import
    issues.

    We have some equivalent methods that do not need to pass the class
    as a parameter, so we can only work with the class name and avoid
    imports that can cause issues.
    """

    @staticmethod
    def is_instance(
        element: object,
        cls: Union[str, type, list]
    ) -> bool:
        """
        Check if the provided 'element' is an instance of the provided
        class (or classes) 'cls'. An instance is not the same as a
        class. The 'cls' parameter can be the class or the string name
        of that class, or a list of them (even mixed).

        This method is useful if you want to check if it belongs to a
        class but without importing the class and passing it as a 
        parameter to avoid cyclic import issues.
        """
        # TODO: Please, simplify this code below but
        # paying attention to avoid infinite loops by
        # reusing other methods of this class

        # 1. Single value and it is a class
        if (
            not PythonValidator.is_list(cls) and
            isinstance(cls, type)
        ):
            return isinstance(element, cls)

        # 2. Single value and it is a string
        if (
            not PythonValidator.is_list(cls) and
            isinstance(cls, str)
        ):
            return getattr(type(element), '__name__', None) == cls
            
        # 3. Multiple values and they are all classes
        if (
            PythonValidator.is_list(cls) and
            all(
                isinstance(cls_item, type)
                for cls_item in cls
            )
        ):
            return any(
                isinstance(element, cls_item)
                for cls_item in cls
            )

        # 4. Multiple values and they are all strings
        if (
            PythonValidator.is_list(cls) and
            all(
                isinstance(cls_item, str)
                for cls_item in cls
            )
        ):
            return getattr(type(element), '__name__', None) in cls

        # 5. Multiple values and they are mixed classes and strings
        if (
            PythonValidator.is_list(cls) and
            all(
                (
                    isinstance(cls_item, str) or
                    isinstance(cls_item, type)
                )
                for cls_item in cls
            )
        ):
            element_class_name = getattr(type(element), '__name__', None)

            cls_str_list = [
                cls_item
                for cls_item in cls
                if isinstance(cls_item, str)
            ]
            cls_classes_list = [
                cls_item
                for cls_item in cls
                if isinstance(cls_item, type)
            ]

            return any(
                (
                    isinstance(element, cls_item)
                    for cls_item in cls_classes_list
                ) or
                (
                    element_class_name in cls_str_list
                )
            )
        
        # TODO: Maybe some parameter provided is invalid
        return False
    
    @staticmethod
    def is_an_instance(
        element: object
    ) -> bool:
        """
        Check if the provided 'element' is an instance of any class.
        """
        return PythonValidator.is_instance(element, object)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is None
    
    @staticmethod
    def is_class(
        element,
        cls: Union[list[Union[type, str]], str, type]
    ) -> bool:
        """
        Check if the provided 'element' is the provided class 'cls'.
        A class is not the same as an instance of that class. The
        'classes' parameter can be the class or the string name of that
        class. 

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if (
            not PythonValidator.is_string(cls) and
            not PythonValidator.is_a_class(cls) and
            not PythonValidator.is_list_of_string(cls) and
            not PythonValidator.is_list_of_classes(cls)
        ):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')

        # To list
        cls = (
            [cls]
            if not PythonValidator.is_list(cls) else
            cls
        )

        # To str
        cls = [
            (
                class_item
                if PythonValidator.is_string(class_item) else
                class_item.__name__ # the name of the class
            ) for class_item in cls
        ]
        
        if PythonValidator.is_string(cls):
            if cls == 'str':
                return PythonValidator.is_string(element)

            # TODO: This is not working at all, I need to check why
            # and to apply more ifs (maybe)
            return getattr(element, '__name__', None) is cls
        
        return (
            PythonValidator.is_a_class(element) and
            element == cls
        )

    @staticmethod
    def is_a_class(
        element: type
    ):
        """
        Check if the provided 'element' is a class.
        """
        return PythonValidator.is_instance(element, type)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is not None
    
    @staticmethod
    def is_subclass(
        element: type,
        cls: Union[str, type]
    ) -> bool:
        """
        Check if the provided 'element' is a subclass of the provided
        class 'cls'. The 'cls' parameter can be the class or the
        string name of that class.

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if (
            not PythonValidator.is_string(cls) and
            not PythonValidator.is_a_class(cls)
        ):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if not PythonValidator.is_a_class(element):
            # We want to know if it is a subclass, we don't
            # care if the provided one is an instance or a class,
            # so we try with both.
            if PythonValidator.is_an_instance(element):
                element = type(element)
            else:
                return False
            
        """
        The element.__mro__ returns a list like this below in
        which you can see, oredered, the classes hierarchy.
        This can be useful, so I keep it here:

        (<class 'yta_multimedia.video.generation.manim.classes.text.simple_text_manim_animation.ExampleManimAnimationGenerator'>, <class 'yta_multimedia.video.generation.manim.classes.base_manim_animation.BaseManimAnimation'>, <class 'manim.scene.scene.Scene'>, <class 'object'>)    
        """
            
        return (
            cls in [
                base_class.__name__
                for base_class in element.__bases__
            ]
            if PythonValidator.is_string(cls) else
            issubclass(element, cls)
        )

    @staticmethod
    def is_a_function(
        element: 'function'
    ) -> bool:
        """
        Check if the provided 'element' is a function.
        """
        # TODO: Maybe inspect.isfunction(element) (?)
        return type(element).__name__ == 'function'
    
    @staticmethod
    def is_class_staticmethod(
        cls: type,
        method: 'function',
        method_name: str = None
    ) -> bool:
        """
        Check if the provided 'method' is an staticmethod (a
        function) defined in the also provided 'cls' class.

        If the 'method_name' parameter is provided, it will
        also check if the name of the provided 'method' is
        equal to the one provided in the 'method_name' param.
        """
        if not PythonValidator.is_a_class(cls):
            raise Exception('The provided "cls" parameter is not a class.')
        
        if not PythonValidator.is_a_function(method):
            raise Exception('The provided "method" parameter is not a function.')
        
        for function in inspect.getmembers(cls, predicate = inspect.isfunction):
            if function[0] == method.__name__:
                return (
                    True                            # It is one staticmethod
                    if method_name is None else
                    method.__name__ == method_name  # It is the specific staticmethod
                )
            
        return False
    
    @staticmethod
    def is_list(
        element: list
    ) -> bool:
        """
        Check if the provided 'element' is a list, which
        is quite different from an array.
        """
        return type(element) == list
    
    @staticmethod
    def is_array(
        element: array
    ) -> bool:
        """
        Check if the provided 'element' is an array, which
        is quite different from a list.
        """
        return type(element) == array

    @staticmethod
    def is_empty_list(
        element: list
    ) -> bool:
        """
        Check if the provided 'element' is a list but empty.
        """        
        return (
            PythonValidator.is_list(element) and
            len(element) == 0
        )
    
    @staticmethod
    def is_list_of_instances(
        element: list[object]
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are instances of any class.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_an_instance(item)
                for item in element
            )
        )
    
    @staticmethod
    def is_list_of_these_instances(
        element: list[object],
        cls: type
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are instances of the provided 'cls'
        class.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_instance(item, cls)
                for item in element
            )
        )
    
    @staticmethod
    def is_list_of_string(
        element: list[str]
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are strings.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_string(item)
                for item in element
            )
        )

    def is_list_of_numbers(
        element: list[Union[int, float]]
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are numbers.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_number(item)
                for item in element
            )
        )

    def is_list_of_positive_numbers(
        element: list[Union[int, float]],
        do_include_zero: bool = True
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are positive numbers.
        """
        from yta_general_utils.programming.validator.number import NumberValidator

        return (
            PythonValidator.is_list(element) and
            all(
                NumberValidator.is_positive_number(item, do_include_zero = do_include_zero)
                for item in element
            )
        )
    
    @staticmethod
    def is_list_of_classes(
        element: list[type]
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are classes.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_a_class(item)
                for item in element
            )
        )

    @staticmethod
    def is_list_of_these_classes(
        element: list[type],
        cls: Union[list[Union[type, str]], str, type]
    ) -> bool:
        """
        Check if the provided 'element' is a list in which
        all the items are classes from the given 'cls' 
        class or class array.
        """
        return (
            PythonValidator.is_list(element) and
            all(
                PythonValidator.is_class(item, cls)
                for item in element
            )
        )

    @staticmethod
    def is_dict(
        element: dict
    ) -> bool:
        """
        Check if the provided 'element' is a dict.
        """
        return PythonValidator.is_instance(element, dict)

    @staticmethod
    def is_tuple(
        element
    ) -> bool:
        """
        Check if the provided 'element' is a tuple.
        """
        return PythonValidator.is_instance(element, tuple)
    
    @staticmethod
    def is_tuple_or_list_or_array_of_n_elements(
        element: Union[tuple, list, array],
        n: int
    ) -> bool:
        """
        Check if the provided 'element' is a tuple or a list
        with 'n' values.
        """
        return (
            (
                PythonValidator.is_tuple(element) or 
                PythonValidator.is_list(element) or
                PythonValidator.is_array(element)
            ) and
            len(element) == n
        )
    
    @staticmethod
    def is_string(
        element: str
    ) -> bool:
        """
        Check if the provided 'element' is a string (str).
        """
        return PythonValidator.is_instance(element, str)
    
    @staticmethod
    def is_boolean(
        element: bool
    ) -> bool:
        """
        Check if the provided 'element' is a boolean (bool).
        """
        return PythonValidator.is_instance(element, bool)
    
    @staticmethod
    def is_number(
        element: Union[int, float, str],
        do_accept_string_number: bool = False
    ) -> bool:
        """
        Check if the provided 'element' is a numeric value. If
        'do_accept_string_number' is True, it will try to parse
        the 'element' as a float if a string is provided.
        """
        from yta_general_utils.programming.validator.number import NumberValidator

        return NumberValidator.is_number(element, do_accept_string_number)
    
    @staticmethod
    def is_numpy_array(
        element: np.ndarray
    ) -> bool:
        """
        Check if the provided 'element' is an instance of the
        numpy array np.ndarray.
        """
        return PythonValidator.is_instance(element, np.ndarray)
    
    @staticmethod
    def is_enum(
        element: Union['YTAEnum', Enum]
    ) -> bool:
        """
        Check if the provided 'element' is a subclass of an Enum or
        a YTAEnum.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: I think it is 'EnumMeta' not Enum
        return (
            PythonValidator.is_subclass(element, 'YTAEnum') or
            PythonValidator.is_subclass(element, 'Enum')
        )
    
    @staticmethod
    def is_enum_instance(
        element: Union['YTAEnum', Enum]
    ) -> bool:
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is an instance.
        """
        return (
            PythonValidator.is_enum(element) and
            PythonValidator.is_an_instance(element)
        )
    
    @staticmethod
    def is_enum_class(
        element: Union['YTAEnum', Enum]
    ) -> bool:
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is a class.
        """
        return (
            PythonValidator.is_enum(element) and
            PythonValidator.is_a_class(element)
        )
    
    @staticmethod
    def is_callable(
        element: callable
    ) -> bool:
        """
        Check if the provided 'element' is a callable
        instance (method, function) or not.
        """
        return callable(element)
    
    # TODO: This method below is not complete, need work
    @staticmethod
    def validate_method_params(
        method: 'function',
        params: list, 
        params_to_ignore: list[str] = ['self', 'cls', 'args', 'kwargs']
    ):
        """
        IMPORTANT! This method should be called on top of any method
        in which you want to validate if the provided parameters are
        valid, by providing the method (function) declaration and
        also the 'locals()' function executed as 'params' parameter.
        So, it should be called like this:

        PythonValidator.validate_method_params(function, locals())

        This method check the types of the params that the provided
        'method' has and validate if the provided values fit the
        specified types (according also to the default values). It
        will raise an Exception when any of the provided params (and
        not ignored) is not valid according to its type declaration.

        The provided 'params' must be a dict containing all the param
        names and values.

        This method is able to parse non-type declarations, as in
        "method(type)", single declarations, as in "method(type: str)"
        and Union declarations, as in
        "method(type: Union[str, MyClass])"

        The 'method' parameter must be a real python method to be able
        to inspect it.
        """
        if not PythonValidator.is_a_function(method):
            raise Exception('The provided "method" parameter is not a valid method (function).')

        # This below is like '<class 'package.of.class.name'> or '<class 'str'>
        SINGLE_TYPE_REGEX = r"<class '([^']+)'>"
        # This below is like 'Union['str', 'int', 'FfmpegHandler']
        UNION_TYPE_REGEX = r"typing\.Union\[\s*((?:[^,]+(?:\s*,\s*)?)+)\s*\]"
        # This below is to flag those params with no default value
        # because None can be a default value indicating that it is
        # an optional value
        NO_DEFAULT_VALUE = '__no_default_value__'
        NO_TYPE = '__no_type__'

        # TODO: Refactor this below to make it easier to be read
        for param in inspect.signature(method).parameters.values():
            if param.name in params_to_ignore:
                continue

            print(param.name)
            print(params_to_ignore)

            types = param.annotation if param.annotation is not inspect.Parameter.empty else NO_TYPE
            default_value = param.default if param.default is not inspect.Parameter.empty else NO_DEFAULT_VALUE

            # 'types' can be nothing, a single type or an Union
            if types:
                match_class = re.match(SINGLE_TYPE_REGEX, str(types))
                match_union = re.match(UNION_TYPE_REGEX, str(types))

                # Turn type to array of string types
                if match_class:
                    types = [match_class.group(1).split('.')[-1]]
                elif match_union:
                    classes = match_union.group(1).split(',')
                    types = [class_i.strip().split('.')[-1] for class_i in classes]

            # Now check with the param provided
            user_param = params.get(param.name, None)

            if types is NO_TYPE and user_param is None:
                # If no type we cannot validate anything, but I 
                # think if no type nor value it will not be
                # executed and this Exception below will never
                # happen
                raise Exception(f'The param "{str(param.name)}" has no type declaration but also None value, so it is not accepted.')
            elif user_param == None and (PythonValidator.is_list(types) and 'None' in types or default_value == None):
                # TODO: If we are strict with typing, a value that
                # can be None should be Union[None, ...] and also
                # param = None (as default value) to indicate it is
                # optional, but we accept both of them separately

                # Param value is None and None is accepted or is
                # default value
                pass
            elif user_param == None:
                raise Exception(f'The param "{str(param.name)}" has None value provided and we expected one of these types: {", ".join(types)}.')
            else:
                if not PythonValidator.is_instance(user_param, types) and types is not NO_TYPE:
                    print(types)
                    types_str = ', '.join(types)
                    raise Exception(f'The param value "{str(param.name)}" provided "{str(user_param)}" is not one of the expected types: {types_str}.')

        return True
